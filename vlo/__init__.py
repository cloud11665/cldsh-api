import json
import os
import time
from enum import Enum
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union
from traceback import format_exc

from fastapi import APIRouter, Path, Query
from pydantic.color import Color

from utils.cache import TimedLRUcache
import schemas
from .lut import LUT, FetchLUT
from .timetable import GetTimetableData, GetNextLesson
from .substitutions import GetSubstitutions

router = APIRouter(prefix="/vlo", tags=["VLO"])

@router.get("/listclass", response_model=List[str])
def ListClass():
	'''
	Returns a sorted array of `str` representing every class in the timetable.\n
	Response model: `List[str]`
	'''
	values = [*LUT["VLO"]["CLASS"]["ID"].values()]
	values.sort()
	return values

@router.get("/timestamps", response_model=Dict[str, schemas.TimeIndex])
def Timestamps():
	'''
	Returns a dictionary of `TimeIndex` objects, which are used for indexing the timetable.\n
	Response model: `Dict[str, TimeIndex]`
	'''
	values = LUT["VLO"]["TIME"]["DATA"]
	return values

@router.get("/ttdata/{class_id}", response_model=List[List[List[schemas.Lesson]]])
@TimedLRUcache(m=30)
def TimetableData(class_id:schemas.ClassID=Path(..., description="The ID of class."),
                  offset:Optional[int]=Query(0, ge=-5, le=5, description="Positive time offset in weeks."),
	                highlight:Optional[bool]=Query(False, description="Reduce the color saturation of every lesson, other than the current."),
	                defaultColor:Optional[Color]=Query(Color("#D0FFD0"), description="Change the default color for lessons without predefined value."),
	                overrideColor:Optional[Color]=Query(None, description="Override every color in the timetable. (works with `highlight`)")):
	'''
	Returns a 5 element array consisting of arrays representing concurrent lesons represented as an array of `Lesson` objects.\n
	Response model: `List[List[List[Lesson]]]`\n
	Cache timeout - 30m
	'''
	return GetTimetableData(class_id.value, offset, highlight, defaultColor, overrideColor)

@router.get("/next/{class_id}", response_model=str)
def NextLesson(class_id:schemas.ClassID=Path(..., description="The ID of class."),
               groups:str=Query(..., description="Comma separated names of selected groups."),
	             style:Optional[schemas.NextStyle]=Query(schemas.NextStyle.Default, description="Display style."),
	             notext:Optional[str]=Query("", description="Text to be displayed, when there are no lessons remaining for the day.")):
	'''
	Returns the next lesson (if there is any) and the ammount of time remaining until it starts.\n
	Response model: `str`
	'''
	groups = groups.split(",")
	return GetNextLesson(class_id.value, groups, style, notext)

@router.get("/substitutions/{class_id}", response_model=List[schemas.Substitution])
@TimedLRUcache(m=30)
def Substitutions(class_id:schemas.ClassID=Path(..., description="The ID of class."),
                  offset:Optional[int]=Query(0, ge=-256, le=256, description="Positive time offset in days.")):
	'''
	Returns an array of `Substitution` objects.\n
	Response model: `List[Substitution]`\n
	Cache timeout - 30m
	'''
	return GetSubstitutions(class_id.value, offset)

@router.put("/updateLUT", response_model=str)
def UpdateLUT():
	'''
	Updates the local look up table used for IDs.\n
	Response model: `str`
	'''
	global LUT
	_LUT = LUT
	try:
		FetchLUT()
	except Exception as e:
		LUT = _LUT
		return format_exc()

	return "LUT update successfull!"

