from serializers.user import embeddedUserResponse

def classEntity(classes) -> dict:
  return {
    "id": str(classes["_id"]),
    "name": classes["name"],
    "description": classes["description"],
    "school": classes["school"],
    "user": str(classes["user"]),
    "setIds": classes["setIds"],
    "permissions": classes["permissions"],
    "created_at": classes["created_at"],
    "updated_at": classes["updated_at"]
  }

def populatedClassEntity(classes) -> dict:
  return {
    "id": str(classes["_id"]),
    "name": classes["name"],
    "description": classes["description"],
    "school": classes["school"],
    "user": embeddedUserResponse(classes["user"]),
    "setIds": classes["setIds"],
    "permissions": classes["permissions"],
    "created_at": classes["created_at"],
    "updated_at": classes["updated_at"]
  }

def classListEntity(classes) -> list:
  return [populatedClassEntity(classItem) for classItem in classes]