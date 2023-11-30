from serializers.user import embeddedUserResponse

def commentEntity(comment) -> dict:
  return {
    "id": str(comment["_id"]),
    "comment": comment["comment"],
    "setId": str(comment["setId"]),
    "user": str(comment["user"]),
    "created_at": comment["created_at"],
    "updated_at": comment["updated_at"]
  }

def populatedCommentEntity(comment) -> dict:
  return {
    "id": str(comment["_id"]),
    "comment": comment["comment"],
    "setId": str(comment["setId"]),
    "user": embeddedUserResponse(comment["user"]),
    "created_at": comment["created_at"],
    "updated_at": comment["updated_at"]
  }

def commentListEntity(comments) -> list:
  return [populatedCommentEntity(comment) for comment in comments]
