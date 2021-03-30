from enum import Enum, IntEnum
from typing import Dict, List, Optional, Union
from datetime import datetime

from pydantic import BaseModel

from vlo.lut import LUT


class Bytes(Enum):
	KiB = "KiB"
	MiB = "MiB"
	GiB = "GiB"
	TiB = "TiB"


class Storage(BaseModel):
	name: str
	unit: Bytes
	used: float
	total: float
	usage: float
	fsystem: Optional[str]


class Cpu(BaseModel):
	freq: int
	cores: int
	usage: float


class HWStat(BaseModel):
	ram: Storage
	disks: List[Storage]
	cpu: Cpu


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


class NextStyle(Enum):
	Default    = "Default"
	Timed      = "Timed"
	Detailed   = "Detailed"


class Comment(BaseModel):
	id: int
	date: datetime
	username: str
	content: str
	avatar: str
	parent_id: int
