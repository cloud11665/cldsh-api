from copy import deepcopy
from pathlib import Path
from traceback import format_exc
from typing import Optional, List

import rapidjson
import schemas
from fastapi import APIRouter, Path, Query
from utils.response import JsonObjResponse, JsonStrResponse

from .lut import LUT, FetchLUT
from .substitutions import GetSubstitutions
from .timetable import GetNextLesson, GetTimetableData

router = APIRouter(prefix="/vlo", tags=["VLO"])

@router.get("/listclass")
async def ListClass():
	'''
	Returns a sorted array of `str` representing every class in the timetable.\n
	Response model: `List[str]`
	'''
	values = [*LUT["VLO"]["CLASS"]["ID"].values()]
	values.sort()
	return JsonObjResponse(values)

@router.get("/timestamps")
async def Timestamps():
	'''
	Returns a dictionary of `TimeIndex` objects, which are used for indexing the timetable.\n
	Response model: `Dict[str, TimeIndex]`
	'''
	values = LUT["VLO"]["TIME"]["DATA"]
	return rapidjson.dumps(values, ensure_ascii=False)

@router.get("/ttdata/{class_id}", response_model=List[List[List[schemas.Lesson]]])
async def TimetableData(class_id:schemas.ClassID= Path(..., description="The ID of class."),
	                  offset:Optional[int]  = Query(0, ge=-5, le=5, description="Positive time offset in weeks."),
	               highlight:Optional[bool] = Query(False, description="Reduce the color saturation of every lesson, other than the current."),
	            defaultColor:Optional[str]  = Query("#D0FFD0", description="Change the default color for lessons without predefined value."),
	           overrideColor:Optional[str]  = Query(None, description="Override every color in the timetable. (works with `highlight`)")):
	'''
	Returns a 5 element array consisting of arrays representing concurrent lesons represented as an array of `Lesson` objects.\n
	Response model: `List[List[List[Lesson]]]`\n
	Cache timeout - 30m
	'''
	return JsonStrResponse(GetTimetableData(
		class_id.value, offset, highlight, defaultColor, overrideColor, True
		))

@router.get("/next/{class_id}")
async def NextLesson(class_id:schemas.ClassID=Path(..., description="The ID of class."),
               groups:str=Query(..., description="Comma separated names of selected groups."),
               style:Optional[str]=Query("0", description="Style bitmask"),
               notext:Optional[str]=Query("", description="Text to be displayed, when there are no lessons remaining for the day.")):
	'''
	Returns the next lesson (if there is any) and the ammount of time remaining until it starts.\n
	\n
	style bitmask breakdown:\n
	- subject_verbose `[no/yes]` **(0 - 1)**\n
	- time_enabled `[no/yes]` **(0 - 1)**\n
	- time_unit `[hours/minutes]` **(0 - 1)**\n
	- time_display_unit `[no/yes]` **(0 - 1)**\n
	- time_separator `[" ", ":", ".", "/"]` **(00 - 11)**\n
	- time_bracket_begin `["<", "{", "[", "(", ""]` **(000 - 111)**\n
	- time_bracket_end   `[">", "}", "]", ")", ""]` **(000 - 111)**\n
	example:\n
	- `011101110110 -> 0x776 -> "776"`\n
	Response model: `str`
	'''
	groups = groups.split(",")
	return GetNextLesson(class_id.value, groups, style, notext)

@router.get("/substitutions/{class_id}")
async def Substitutions(class_id:schemas.ClassID=Path(..., description="The ID of class."),
                  offset:Optional[int]=Query(0, ge=-256, le=256, description="Positive time offset in days.")):
	'''
	Returns an array of `Substitution` objects.\n
	Response model: `List[Substitution]`\n
	Cache timeout - 30m
	'''
	return JsonStrResponse(GetSubstitutions(
		class_id.value, offset, True))

#@router.put("/updateLUT")
#async def UpdateLUT():
#	'''
#	Updates the local look up table used for IDs.\n
#	Response model: `str`
#	'''
#	global LUT
#	_LUT = deepcopy(LUT)
#	try:
#		FetchLUT()
#	except Exception as e:
#		LUT = _LUT
#		return format_exc()
#
#	return "LUT update successfull!"

