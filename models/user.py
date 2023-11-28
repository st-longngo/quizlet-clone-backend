from datetime import datetime
from typing import List
from pydantic import BaseModel, constr
from bson.objectid import ObjectId

class UserBase(BaseModel):
    name: str
    username: str
    email: str
    photo: str or None = None
    country: str or None = None
    phone: str or None = None
    role: str or None = None
    created_at: datetime or None = None
    updated_at: datetime or None = None

    class Config:
        orm_mode = True


class CreateUser(UserBase):
    password: constr(min_length=8)
    passwordConfirm: str

class LoginUser(BaseModel):
    username: str
    password: constr(min_length=8)

class UserResponseBase(UserBase):
    id: str
    pass

class UserResponse(BaseModel):
    status: str
    user: UserResponseBase

class FilteredUserResponse(UserBase):
    id: str

class ListUserResponse(BaseModel):
  status: str
  results: int
  users: List[UserResponseBase]

class UpdateUser(BaseModel):
  name: str or None = None
  username: str or None = None
  photo: str or None = None
  country: str or None = None
  phone: str or None = None

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}

class ChangePasswordUser(BaseModel):
   currentPassword: str
   newPassword: str
   confirmPassword: str

   class Config:
      orm_mode = True
  