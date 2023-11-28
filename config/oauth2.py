import base64
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from bson.objectid import ObjectId

from serializers.user import userEntity

from .database import User

class Settings(BaseModel):
  JWT_PUBLIC_KEY: str = 'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUZ3d0RRWUpLb1pJaHZjTkFRRUJCUUFEU3dBd1NBSkJBSSs3QnZUS0FWdHVQYzEzbEFkVk94TlVmcWxzMm1SVgppUFpSclRaY3d5eEVYVURqTWhWbi9KVHRsd3h2a281T0pBQ1k3dVE0T09wODdiM3NOU3ZNd2xNQ0F3RUFBUT09Ci0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ=='
  JWT_PRIVATE_KEY: str = 'LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlCT2dJQkFBSkJBSSs3QnZUS0FWdHVQYzEzbEFkVk94TlVmcWxzMm1SVmlQWlJyVFpjd3l4RVhVRGpNaFZuCi9KVHRsd3h2a281T0pBQ1k3dVE0T09wODdiM3NOU3ZNd2xNQ0F3RUFBUUpBYm5LaENOQ0dOSFZGaHJPQ0RCU0IKdmZ2ckRWUzVpZXAwd2h2SGlBUEdjeWV6bjd0U2RweUZ0NEU0QTNXT3VQOXhqenNjTFZyb1pzRmVMUWlqT1JhUwp3UUloQU84MWl2b21iVGhjRkltTFZPbU16Vk52TGxWTW02WE5iS3B4bGh4TlpUTmhBaUVBbWRISlpGM3haWFE0Cm15QnNCeEhLQ3JqOTF6bVFxU0E4bHUvT1ZNTDNSak1DSVFEbDJxOUdtN0lMbS85b0EyaCtXdnZabGxZUlJPR3oKT21lV2lEclR5MUxaUVFJZ2ZGYUlaUWxMU0tkWjJvdXF4MHdwOWVEejBEWklLVzVWaSt6czdMZHRDdUVDSUVGYwo3d21VZ3pPblpzbnU1clBsTDJjZldLTGhFbWwrUVFzOCtkMFBGdXlnCi0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0t'
  REFRESH_TOKEN_EXPIRES_IN: int = 60
  ACCESS_TOKEN_EXPIRES_IN: int = 60
  JWT_ALGORITHM: str = 'RS256'

  authjwt_algorithm: str = JWT_ALGORITHM
  authjwt_decode_algorithms: List[str] = [JWT_ALGORITHM]
  authjwt_token_location: set = {'cookies', 'headers'}
  authjwt_access_cookie_key: str = 'access_token'
  authjwt_refresh_cookie_key: str = 'refresh_token'
  authjwt_cookie_csrf_protect: bool = False
  authjwt_public_key: str = base64.b64decode(
      JWT_PUBLIC_KEY).decode('utf-8')
  authjwt_private_key: str = base64.b64decode(
      JWT_PRIVATE_KEY).decode('utf-8')


@AuthJWT.load_config
def get_config():
  return Settings()


class NotVerified(Exception):
  pass


class UserNotFound(Exception):
  pass


def require_user(Authorize: AuthJWT = Depends()):
  try:
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = userEntity(User.find_one({'_id': ObjectId(str(user_id))}))

    if not user:
      raise UserNotFound('User no longer exist')

  except Exception as e:
    error = e.__class__.__name__
    print(error)
    if error == 'MissingTokenError':
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
    if error == 'UserNotFound':
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED, detail='User no longer exist')
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')
  return user_id
