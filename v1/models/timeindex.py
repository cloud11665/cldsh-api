from pydantic import BaseModel

class TimeIndex(BaseModel):
	begin: str
	end: str