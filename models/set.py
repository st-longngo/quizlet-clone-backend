from pydantic import BaseModel
from bson.objectid import ObjectId
from typing import List
from models import user

from datetime import datetime

class SetDataBase(BaseModel):
    front: str
    back: str
    image: str

    class Config:
        orm_mode = True

class SetBase(BaseModel):
  name: str
  description: str
  data: List[SetDataBase]
  created_at: datetime or None = None
  updated_at: datetime or None = None

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}


class CreateSet(SetBase):
  user: str or None = None
  pass


class SetResponse(SetBase):
  id: str
  user: user.FilteredUserResponse
  created_at: datetime
  updated_at: datetime


class UpdateSet(BaseModel):
  name: str or None = None
  description: str or None = None
  data: List[SetDataBase] or None = None

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}

class ListSetResponse(BaseModel):
  status: str
  results: int
  posts: List[SetResponse]
  