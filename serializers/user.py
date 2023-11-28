def userEntity(user) -> dict:
  return {
    "id": str(user["_id"]),
    "name": user["name"],
    "username": user["username"],
    "email": user["email"],
    "role": user["role"],
    "photo": user["photo"],
    "phone": user["phone"],
    "country": user["country"],
    "password": user["password"],
    "created_at": user["created_at"],
    "updated_at": user["updated_at"]
  }


def userResponseEntity(user) -> dict:
  return {
    "id": str(user["_id"]),
    "name": user["name"],
    "username": user["username"],
    "email": user["email"],
    "role": user["role"],
    "photo": user["photo"],
    "phone": user["phone"],
    "country": user["country"],
    "created_at": user["created_at"],
    "updated_at": user["updated_at"]
  }


def embeddedUserResponse(user) -> dict:
  return {
    "id": str(user["_id"]),
    "name": user["name"],
    "email": user["email"],
    "photo": user["photo"],
    "phone": user["phone"],
    "country": user["country"],
  }


def userListEntity(users) -> list:
  return [userEntity(user) for user in users]
