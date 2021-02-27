import datetime
import random

import requests
from bs4 import BeautifulSoup

from .lut import LUT
import schemas

def GetSubstitutions(klass:str, offset:int):
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

	classes = {}
	soup = BeautifulSoup(resp.json()["r"], features="lxml")

	for clsa in soup.find_all("div", class_="section print-nobreak"):
		cls_name = clsa.find("span", class_="print-font-resizable").text
		rm_list = []

		for removed in clsa.find_all("div", class_="row remove"):
			div_idx = removed.find("div", class_="period")
			span_idx = div_idx.find("span", class_="print-font-resizable")
			span_idx = span_idx.text

			div_info = removed.find("div", class_="info")
			span_info = div_info.find("span", class_="print-font-resizable")
			span_info = span_info.text

			rm_list.append(schemas.Substitution(time_signature=span_idx,
	                                comment=span_info))

		classes[cls_name] = rm_list

	if klass:
		return classes.get(klass, [])
	return classes