import datetime
import json
from pathlib import Path

import requests

_PATH = Path("./vlo")
LUT = json.load((_PATH / "lut.json").open("r", encoding="utf8"))

def FetchLUT():
	today = datetime.datetime.today()
	year = today.year
	last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)
	next_friday = last_monday + datetime.timedelta(days=4)

	resp = requests.post(
		url="https://v-lo-krakow.edupage.org/rpr/server/maindbi.js?__func=mainDBIAccessor",
		headers={
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
			"Referer": "https://v-lo-krakow.edupage.org/timetable/"
		},
		json={
			"__args": [
				None,
				2020,
				{
					"vt_filter": {
						"datefrom": last_monday.strftime("%Y-%m-%d"),
						"dateto": next_friday.strftime("%Y-%m-%d")
					}
				},
				{
					"op": "fetch",
					"tables": [],
					"columns":[],
					"needed_part": {
						"teachers": ["__name","short"],
						"classes": ["__name","classroomid"],
						"classrooms":["__name","name","short"],
						"igroups":["__name"],
						"students":["__name","classid"],
						"subjects":["__name","name","short"],
						"events":["typ","name"],
						"event_types":["name"],
						"subst_absents":["date","absent_typeid","groupname"],
						"periods":["__name","period","starttime","endtime"],
						"dayparts":["starttime","endtime"],
						"dates":["tt_num","tt_day"]
					},
					"needed_combos":{},
					"client_filter":{},
					"info_tables":[],
					"info_columns":[],
					"has_columns":{}
				}
			],
			"__gsh":"00000000"
		}
	)

	LUT = {
		"AGENTS": [
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"
		],
		"VLO": {
			"TEACHERS": {
				"ID": {
					"SHORT": {}
				}
			},
			"SUBJECTS": {
				"ID": {
					"SHORT": {},
					"LONG": {}
				}
			},
			"CLASS": {
				"ROOM": {
					"ID": {}
				},
				"IDR": {},
				"ID": {}
			},
			"TIME": {
				"DATA": {},
				"RMAP": {},
				"MAP": {}
			}
		}
	}

	resp_json = resp.json()["r"]
	for teacher in resp_json["tables"][0]["data_rows"]:
		x,y = teacher.values()
		LUT["VLO"]["TEACHERS"]["ID"]["SHORT"][x] = y

	for subj in resp_json["tables"][1]["data_rows"]:
		x,y,z = subj.values()
		LUT["VLO"]["SUBJECTS"]["ID"]["LONG"][x] = y
		LUT["VLO"]["SUBJECTS"]["ID"]["SHORT"][x] = z

	for clasrm in resp_json["tables"][2]["data_rows"]:
		x,y = clasrm.values()
		LUT["VLO"]["CLASS"]["ROOM"]["ID"][x] = y

	#Classes
	for klass in resp_json["tables"][3]["data_rows"]:
		x,y,_ = klass.values()
		LUT["VLO"]["CLASS"]["ID"][x] = y
		LUT["VLO"]["CLASS"]["IDR"][y] = x

	for time in resp_json["tables"][6]["data_rows"]:
		x,_,_,_,y,z = time.values()
		LUT["VLO"]["TIME"]["DATA"][x] = {"begin":y,"end":z}
		LUT["VLO"]["TIME"]["MAP"][y] = x
		LUT["VLO"]["TIME"]["RMAP"][x] = y

	with (_PATH / "lut.json").open("w", encoding="utf8") as f:
		json.dump(LUT,f,ensure_ascii=False)

FetchLUT()