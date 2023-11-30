from pydantic import BaseModel
from datetime import datetime
from typing import List

from models import user

class CommentBase(BaseModel):
  comment: str
  created_at: datetime or None = None
  updated_at: datetime or None = None

class CreateComment(CommentBase):
  setId: str or None = None
  user: str or None = None
  pass

class CommentResponse(CommentBase):
  id: str
  comment: str
  user: user.FilteredUserResponse
  created_at: datetime
  updated_at: datetime

class ListSetResponse(BaseModel):
  status: str
  results: int
  comments: List[CommentResponse]