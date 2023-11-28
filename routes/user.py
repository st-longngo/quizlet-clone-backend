from fastapi import APIRouter, Depends, HTTPException, status
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument
from serializers.user import userResponseEntity, userListEntity

from config.database import User
from models import user
from config.oauth2 import require_user

router = APIRouter()

@router.get('/me', response_model=user.UserResponse)
def get_me(user_id: str = Depends(require_user)):
    user = userResponseEntity(User.find_one({'_id': ObjectId(str(user_id))}))
    return {"status": "success", "user": user}

@router.get('/')
def get_users(limit: int = 10, page: int = 1, search: str = '',) :
    print(search)
    pipeline = [
        {'$match': {'username': {'$regex': search}}},
    ]
    users = userListEntity(User.aggregate(pipeline))
    return {'status': 'success', 'results': len(users), 'users': users}

@router.put('/{id}')
def update_user(id: str, payload: user.UpdateUser, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")

    updated_user = User.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)

    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with this id: {id} found')
    return userResponseEntity(updated_user)
