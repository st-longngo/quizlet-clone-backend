from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from models.classes import CreateClass, UpdateClass
from config.database import Class
from config.oauth2 import require_user
from serializers.classes import classEntity, classListEntity
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

router = APIRouter()

@router.get('/')
def get_classes(limit: int = 10, page: int = 1, search: str = ''):
    # skip = (page - 1) * limit
    print(search)
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
    classes = classListEntity(Class.aggregate(pipeline))
    return {'status': 'success', 'results': len(classes), 'classes': classes}

@router.get('/_by-users/{user_id}')
def get_classes_by_user_id(user_id: str = Depends(require_user)):
    pipeline = [
        {'$match': { 'user': ObjectId(user_id)}},
        {'$lookup': {'from': 'users', 'localField': 'user',
                     'foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
    ]
    classes = classListEntity(Class.aggregate(pipeline))
    return {'status': 'success', 'results': len(classes), 'classes': classes}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_class(classes: CreateClass, user_id: str = Depends(require_user)):
    classes.user = ObjectId(user_id)
    classes.created_at = datetime.utcnow()
    classes.updated_at = classes.created_at
    try:
        result = Class.insert_one(classes.dict())
        pipeline = [
            {'$match': {'_id': result.inserted_id}},
            {'$lookup': {'from': 'users', 'localField': 'user',
                         'foreignField': '_id', 'as': 'user'}},
            {'$unwind': '$user'},
        ]
        new_post = classListEntity(Class.aggregate(pipeline))[0]
        return new_post
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Class with name: '{classes.name}' already exists")


@router.put('/{id}')
def update_class(id: str, payload: UpdateClass, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    updated_class = Class.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if not updated_class:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No class with this id: {id} found')
    return classEntity(updated_class)


@router.get('/{id}')
def get_class(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    pipeline = [
        {'$match': {'_id': ObjectId(id)}},
        {'$lookup': {'from': 'users', 'localField': 'user',
                     'foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
    ]
    db_cursor = Class.aggregate(pipeline)
    results = list(db_cursor)

    if len(results) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No class with this id: {id} found")

    classes = classListEntity(results)[0]
    return classes


@router.delete('/{id}')
def delete_class(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    classes = Class.find_one_and_delete({'_id': ObjectId(id)})
    if not classes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No class with this id: {id} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
