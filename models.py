from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UnicodeText
from sqlalchemy.orm import relationship

from database import Base


class Comment(Base):
	__tablename__ = "comments"

	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	date = Column(DateTime)
	username = Column(UnicodeText)
	content = Column(UnicodeText)
	avatar = Column(UnicodeText)
	parent_id = Column(Integer)

	def __iter__(self):
		yield "id", self.id,
		yield "date", self.date,
		yield "username", self.username,
		yield "content", self.content,
		yield "avatar", self.avatar
		yield "parent_id", self.parent_id
