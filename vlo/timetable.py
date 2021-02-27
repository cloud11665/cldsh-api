import datetime
import random
import itertools
from typing import List
import json
import os

import requests

import utils.colors as colors
import schemas
from .lut import LUT
from utils.cache import TimedLRUcache

@TimedLRUcache(m=30)
def GetTimetableData(_klass:str, offset:int=0,
	                   highlight:bool=False,
	                   defaultColor:str="#d0ffd0",
	                   overrideColor:str=None):
	today = datetime.date.today()
	now = datetime.datetime.now() + datetime.timedelta(hours=3)

	last_monday = today + datetime.timedelta(days=-today.weekday())
	next_friday = last_monday + datetime.timedelta(days=4)

	last_monday += datetime.timedelta(weeks=offset)
	next_friday += datetime.timedelta(weeks=offset)

	resp = requests.post(
		url="https://v-lo-krakow.edupage.org/timetable/server/currenttt.js?__func=curentttGetData",
		headers={
			"User-Agent": random.choice(LUT["AGENTS"]),
			"Origin": "https://v-lo-krakow.edupage.org",
			"Referer": "https://v-lo-krakow.edupage.org/timetable/",
			"dnt": "1",
			"sec-fetch-site": "same-origin"
		},
		json={
			"__args": [
				None,
				{
					"year": 2020,
					"datefrom": last_monday.strftime("%Y-%m-%d"),
					"dateto": next_friday.strftime("%Y-%m-%d"),
					"id": LUT["VLO"]["CLASS"]["IDR"][_klass.upper()],
					"showColors": True,
					"showIgroupsInClasses": True,
					"showOrig": True,
					"table": "classes"
				},
			],
			"__gsh": "00000000",
		}
	)

	if not resp.ok:
		return [[],[],[],[],[]]

	data = resp.json()["r"]["ttitems"]

	for i,obj in enumerate(data):
		year, month, day = [int(x) for x in obj["date"].split("-")]
		day_idx = datetime.date(year, month, day) - last_monday
		day_idx = day_idx.days

		if int(obj["starttime"].split(":")[0]) < 7 and int(obj["endtime"].split(":")[0]) > 17:
			obj["starttime"] = "07:10"
			obj["endtime"] = "17:15"
			obj["durationperiods"] = 11

		time_idx = obj.get("starttime")
		time_idx = int(LUT["VLO"]["TIME"]["MAP"].get(time_idx, "0"))

		color    = obj.get("colors", [defaultColor])[0]
		durr     = int(obj.get("durationperiods", 1))
		group    = obj.get("groupnames", [""])
		group    = "".join(group)
		date     = obj.get("date")

		subj_id  = obj.get("subjectid", "0")
		subj     = LUT["VLO"]["SUBJECTS"]["ID"]["LONG"].get(subj_id, "")
		subj     = obj.get("name", subj)           # Don"t question why this works.
		subjs    = LUT["VLO"]["SUBJECTS"]["ID"]["SHORT"].get(subj_id, "")
		subjs    = obj.get("name", subjs)          # It just does...

		teach_id = "".join(obj.get("teacherids", ["0"]))
		teach    = LUT["VLO"]["TEACHERS"]["ID"]["SHORT"].get(teach_id, "")

		klass_id = "".join(obj.get("classroomids", ["0"]))
		klass    = LUT["VLO"]["CLASS"]["ROOM"]["ID"].get(klass_id, "")

		if overrideColor:
			color = overrideColor

		if highlight:
			if day_idx != today.weekday():
				color = colors.grayscale(color, 0.7)
			else:
				hourmin = map(int, LUT["VLO"]["TIME"]["RMAP"][str(time_idx)].split(":"))
				start = datetime.datetime(year, month, day, *hourmin)
				if (now - start).seconds > (3600*3/4) * durr:
					color = colors.grayscale(color, 0.7)


		data[i] = {
			"subject": subj,       #str
			"subject_short": subjs,#str
			"teacher": teach,      #str
			"classroom": klass,    #str
			"color": color,        #str
			"time_index": time_idx,#int
			"duration": durr,      #int
			"group": group,        #str
			"date": date,          #str
			"day_index": day_idx   #int
		}

	days = []
	for _,y in itertools.groupby(data, lambda x: x["day_index"]):
		days.append(list(y))

	buff = [[],[],[],[],[]]

	for i, day in enumerate(days):
		for x, y in itertools.groupby(day, lambda x: x["time_index"]):
				buff[i].append(list(y))

	return buff

def GetNextLesson(klass:str, groups:List[str], style:schemas.NextStyle, notext:str=""):
	now = datetime.datetime.now()

	if now.weekday() < 5:
		resp = GetTimetableData(klass)[now.weekday()]

		filtered = []

		for lesson in resp:
			for index in lesson:
				if index["group"] in groups or index["group"] == "":
					date = index["date"]
					date = date.split("-")
					date = [*map(int, date)]
					time = LUT["VLO"]["TIME"]["RMAP"][str(index["time_index"])]
					time = time.split(":")
					time = [*map(int, time)]

					start = datetime.datetime(*date,*time)

					if start > now:
						delta = start-now

						delta = datetime.timedelta(seconds=delta.seconds)

						index["delta"] = delta
						filtered.append(index)

		lowest = sorted(filtered, key=lambda x: x["delta"])

		if not lowest:
			return notext

		if style.value == schemas.NextStyle.Default.value:
			return f"{lowest[0]['subject_short']}"

		if style.value == schemas.NextStyle.Detailed.value:
			return f"{lowest[0]['subject']}"

		if style.value == schemas.NextStyle.Timed.value:
			minutes, _ = divmod(lowest[0]["delta"].seconds, 60)
			hours, minutes = divmod(minutes, 60)
			return f"{lowest[0]['subject']} [{hours}:{minutes}]"

	return notext