import html
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Form, Path, Query
from requests import get
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/articles", tags=["ARTICLES"])

# Dependency
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@router.get("/{article_id}/ListComments", response_model=List[schemas.Comment])
def GetComments(article_id:int      = Path(..., title="Article ID"),
	              limit:Optional[int] = Query(128, gt=0, title="Maximum number of messages returned.", description="Defaults to 128."),
	              db:Session          = Depends(get_db)):
	'''
	Returns an array of `Comment` objects.\n
	Response model: `List[Comment]`
	'''
	query = db.query(models.Comment) \
	          .filter(models.Comment.parent_id == article_id) \
	          .all()
	query = list(reversed(query))[:limit]
	return [dict(q) for q in query]


@router.post("/{article_id}/AddComment", response_model=schemas.Comment)
def AddComment(article_id:int = Path(..., title="Article ID"),
	             username:str   = Form(..., min_lenght=3, max_length=32),
	             content:str    = Form(..., max_length=2048),
	             db:Session     = Depends(get_db)):
	'''
	Adds a comment to an article.\n
	Response model: `Comment`
	'''
	content = html.escape(content, True)
	username = html.escape(username, True)

	if get(f"https://github.com/{username}.png").ok:
		avatar = f"https://github.com/{username}.png"
	else:
		avatar = ""

	now = datetime.now()
	db_comment = models.Comment(username=username, content=content,
	                            date=now, parent_id=article_id, avatar=avatar)
	db.add(db_comment)
	db.commit()
	db.refresh(db_comment)
	return dict(db_comment)
