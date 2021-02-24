from pydantic import BaseModel

class Substitution(BaseModel):
	time_index: int
	subject: str
	status: str