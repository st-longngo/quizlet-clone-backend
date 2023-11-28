from pydantic import BaseModel
from bson.objectid import ObjectId
from typing import List
from models import user

from datetime import datetime

class PostBase(BaseModel):
  title: str
  content: str
  category: str
  image: str
  created_at: datetime or None = None
  updated_at: datetime or None = None

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}


class CreatePost(PostBase):
  user: str or None = None
  pass


class PostResponse(PostBase):
  id: str
  user: user.FilteredUserResponse
  created_at: datetime
  updated_at: datetime


class UpdatePost(BaseModel):
  title: str or None = None
  content: str or None = None
  category: str or None = None
  image: str or None = None
  user: str or None = None

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}


class ListPostResponse(BaseModel):
  status: str
  results: int
  posts: List[PostResponse]