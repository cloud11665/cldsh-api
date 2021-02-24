from pydantic import BaseModel

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