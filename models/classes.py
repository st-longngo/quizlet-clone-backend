from pydantic import BaseModel
from bson.objectid import ObjectId
from typing import List
from models import user

from datetime import datetime

class ClassBase(BaseModel):
  name: str
  description: str
  school: str
  setIds: List[str]
  permissions: bool or None = False
  created_at: datetime or None = None
  updated_at: datetime or None = None

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}

class CreateClass(ClassBase):
  user: str or None = None
  pass

class ClassResponse(ClassBase):
  id: str
  user: user.FilteredUserResponse
  created_at: datetime
  updated_at: datetime

class UpdateClass(BaseModel):
  name: str or None = None
  description: str or None = None
  school: str or None = None
  setIds: List[str] or None = None
  permissions: bool or None = None

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}

class ListPostResponse(BaseModel):
  status: str
  results: int
  posts: List[ClassResponse]