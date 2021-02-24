import json
import os
import time
from enum import Enum
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union

from fastapi import APIRouter, Path, Query
from pydantic.color import Color

from utils.cache import TimedLRUcache
from ..models.classid import ClassID
from ..models.lesson import Lesson
from ..models.timeindex import TimeIndex
from ..models.nextstyle import NextStyle
from .lut import LUT
from .timetable import GetTimetableData, GetNextLesson

router = APIRouter(prefix="/vlo")

@router.get("/listclass", response_model=List[str])
def ListClass():
	'''
	Returns a sorted array of `str` representing every class in the timetable.\n\n
	Response model: `List[str]`
	'''
	values = [*LUT["VLO"]["CLASS"]["ID"].values()]
	values.sort()
	return values

@router.get("/timestamps", response_model=Dict[str, TimeIndex])
def Timestamps():
	'''
	Returns a dictionary of `TimeIndex` objects, which are used for indexing the timetable.\n\n
	Response model: `Dict[str, TimeIndex]`
	'''
	values = LUT["VLO"]["TIME"]["DATA"]
	return values

@router.get("/ttdata/{class_id}", response_model=List[List[List[Lesson]]])
def TimetableData(class_id:ClassID=Path(..., description="The ID of class."),
                  offset:Optional[int]=Query(0, ge=-5, le=5, description="Positive time offset in weeks."),
									highlight:Optional[bool]=Query(False, description="Reduce the color saturation of every lesson, other than the current."),
									defaultColor:Optional[Color]=Query(Color("#D0FFD0"), description="Change the default color for lessons without predefined value."),
									overrideColor:Optional[Color]=Query(None, description="Override every color in the timetable. (works with `highlight`)")):
	'''
	Returns a 5 element list consisting of lists representing concurrent lesons represented as a list of `Lesson` objects.\n\n
	Response model: `List[List[List[Lesson]]]`
	'''
	return GetTimetableData(class_id.value, offset, highlight, defaultColor, overrideColor)

@router.get("/next/{class_id}")# response_model=str)
def NextLesson(class_id:ClassID=Path(..., description="The ID of class."),
               groups:str=Query(..., description="Comma separated names of selected groups."),
							 style:Optional[NextStyle]=Query(NextStyle.Default, description="Display style."),
							 notext:Optional[str]=Query("", description="Text to be displayed, when there are no lessons remaining for the day.")):
	groups = groups.split(",")
	return GetNextLesson(class_id, groups, style, notext)
