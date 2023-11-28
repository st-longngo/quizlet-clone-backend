from serializers.user import embeddedUserResponse

def setEntity(set) -> dict:
  return {
    "id": str(set["_id"]),
    "name": set["name"],
    "description": set["description"],
    "data": set["data"],
    "user": str(set["user"]),
    "created_at": set["created_at"],
    "updated_at": set["updated_at"]
  }

def populatedSetEntity(set) -> dict:
  return {
    "id": str(set["_id"]),
    "name": set["name"],
    "description": set["description"],
    "data": set["data"],
    "user": embeddedUserResponse(set["user"]),
    "created_at": set["created_at"],
    "updated_at": set["updated_at"]
  }

def setListEntity(sets) -> list:
  return [populatedSetEntity(set) for set in sets]