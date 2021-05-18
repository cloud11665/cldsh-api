from enum import Enum

from pydantic import BaseModel

from vlo.lut import LUT

ClassID = Enum("ClassID", {x:x for x in LUT["VLO"]["CLASS"]["IDR"].keys()})

class Lesson(BaseModel):
	subject: str
	subject_short: str
	teacher: str
	classroom: str
	color: str
	time_index: int
	duration: int
	group: str
	date: str
	day_index: int

class TimeIndex(BaseModel):
	begin: str
	end: str

class Substitution(BaseModel):
	time_signature: str
	comment: str
