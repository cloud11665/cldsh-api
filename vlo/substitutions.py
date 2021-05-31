import datetime
from pprint import pprint
import random

import requests
from bs4 import BeautifulSoup

from .lut import LUT
import rapidjson
import schemas

def GetSubstitutions(klass:str, offset:int, json_=False):
	date_today = datetime.datetime.today() + datetime.timedelta(days=offset)

	resp = requests.post(
		"https://v-lo-krakow.edupage.org/substitution/server/viewer.js?__func=getSubstViewerDayDataHtml",
		headers={
			"User-Agent": random.choice(LUT["AGENTS"]),
			"Origin": "https://v-lo-krakow.edupage.org",
			"Referer": "https://v-lo-krakow.edupage.org/substitution/",
		},
		json={
			"__args": [
				None,
				{
					"date": date_today.strftime("%Y-%m-%d"),
					"mode": "classes"
				}
			],
			"__gsh": "00000000",
		},
	)

	#print(resp.json()["r"], file=open("a.html","w",encoding="utf-8"))

	classes = {}
	soup = BeautifulSoup(resp.json()["r"], features="lxml")

	for clsa in soup.find_all("div", class_="section print-nobreak"):
		cls_name = clsa.find("span", class_="print-font-resizable").text
		rm_list = []

		for removed in clsa.find_all("div", class_="row"):
			div_idx = removed.find("div", class_="period")
			span_idx = div_idx.find("span", class_="print-font-resizable")
			span_idx = span_idx.text

			div_info = removed.find("div", class_="info")
			span_info = div_info.find("span", class_="print-font-resizable")
			span_info = span_info.text

			rm_list.append({
				"time_signature":span_idx, "comment":span_info
			})

		classes[cls_name] = rm_list

	if klass:
		out = classes.get(klass, [])
	else:
		out = classes

	if json_:
		return rapidjson.dumps(out)

	return out