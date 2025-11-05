import os
from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from services.user import UserService
from repo.provider import provide_user_service, provide_ram_storage
from schemas.token import AccessEncode
import helpers.auth as auth
from models.user import User
from repo.ramStorage import RamStorage

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login-form") 
WWW_AUTH = {'WWW-Authenticate': 'Bearer realm="api", error="invalid_token"'}
#TTL = int(os.getenv("REFRESH_EXPIRE_DAYS", 7))*24*60*60

async def get_current_user_oauth2(token: str = Depends(oauth2_scheme), service: UserService = Depends(provide_user_service), ramStorage: RamStorage = Depends(provide_ram_storage)) -> User:
    payload = auth.decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers=WWW_AUTH
        )
    
    try:
        schema = AccessEncode.model_validate(payload)
    except ValidationError:
        raise HTTPException(status_code=401, detail="invalid token payload", headers=WWW_AUTH)
    res = await ramStorage.contains(schema.user_id, schema.sid)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=res,
            headers=WWW_AUTH
        )

    user = await service.get_user(schema.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="user was not found")
    
    return user



    
