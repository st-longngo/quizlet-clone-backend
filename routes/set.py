from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from models.set import CreateSet, UpdateSet
from models.comment import CreateComment
from config.database import Set, Comment
from config.oauth2 import require_user
from serializers.set import setEntity, setListEntity
from serializers.comment import commentListEntity
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

router = APIRouter()

@router.get('/')
def get_sets(limit: int = 10, page: int = 1, search: str = ''):
    # skip = (page - 1) * limit
    pipeline = [
        {'$match': {'name': {'$regex': search}}},
        {'$lookup': {'from': 'users', 'localField': 'user',
                     'foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
        # {
        #     '$skip': skip
        # }, {
        #     '$limit': limit
        # }
    ]
    sets = setListEntity(Set.aggregate(pipeline))
    return {'status': 'success', 'results': len(sets), 'sets': sets}


@router.get('/_by-users/{user_id}')
def get_sets_by_user_id(user_id: str = Depends(require_user)):
    pipeline = [
        {'$match': { 'user': ObjectId(user_id)}},
        {'$lookup': {'from': 'users', 'localField': 'user',
                     'foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
    ]
    sets = setListEntity(Set.aggregate(pipeline))
    return {'status': 'success', 'results': len(sets), 'sets': sets}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_set(set: CreateSet, user_id: str = Depends(require_user)):
    set.user = ObjectId(user_id)
    set.created_at = datetime.utcnow()
    set.updated_at = set.created_at
    try:
        result = Set.insert_one(set.dict())
        pipeline = [
            {'$match': {'_id': result.inserted_id}},
            {'$lookup': {'from': 'users', 'localField': 'user',
                         'foreignField': '_id', 'as': 'user'}},
            {'$unwind': '$user'},
        ]
        new_post = setListEntity(Set.aggregate(pipeline))[0]
        return new_post
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Set with name: '{set.name}' already exists")


@router.put('/{id}')
def update_set(id: str, payload: UpdateSet, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    updated_set = Set.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if not updated_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No set with this id: {id} found')
    return setEntity(updated_set)


@router.get('/{id}')
def get_set(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    pipeline = [
        {'$match': {'_id': ObjectId(id)}},
        {'$lookup': {'from': 'users', 'localField': 'user',
                     'foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
    ]
    db_cursor = Set.aggregate(pipeline)
    results = list(db_cursor)

    if len(results) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No set with this id: {id} found")

    sets = setListEntity(results)[0]
    return sets


@router.delete('/{id}')
def delete_set(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    set = Set.find_one_and_delete({'_id': ObjectId(id)})
    if not set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No set with this id: {id} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/{id}/comments')
def get_comment(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    pipeline = [
        {'$match': {'setId': ObjectId(id)}},
        {'$lookup': {'from': 'users', 'localField': 'user',
                     'foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
    ]
    db_cursor = Comment.aggregate(pipeline)
    results = list(db_cursor)

    comments = commentListEntity(results)
    return comments

@router.post('/{id}/comments', status_code=status.HTTP_201_CREATED)
def create_comment(id: str, comment: CreateComment, user_id: str = Depends(require_user)):
    comment.user = ObjectId(user_id)
    comment.setId = ObjectId(id)
    comment.created_at = datetime.utcnow()
    comment.updated_at = comment.created_at
    try:
        result = Comment.insert_one(comment.dict())
        pipeline = [
            {'$match': {'_id': result.inserted_id}},
            {'$lookup': {'from': 'users', 'localField': 'user',
                         'foreignField': '_id', 'as': 'user'}},
            {'$unwind': '$user'},
        ]
        new_comment = commentListEntity(Comment.aggregate(pipeline))[0]
        return new_comment
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Comment already exists")
    
@router.delete('/{comment_id}/comments')
def delete_set(comment_id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(comment_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    comment = Comment.find_one_and_delete({'_id': ObjectId(comment_id)})
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No comment with this id: {id} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
