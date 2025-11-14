from datetime import datetime, timezone
import os
from typing import Any
from repo.ramStorage import RamStorage
from repo.uow import UnitOfWork
from schemas.user import UserCreate, UserLogin, UserLoginResponce
import helpers.password as password_helper
import helpers.auth as auth
import helpers.cookie as cookie
from fastapi import HTTPException, Response, status, Request
from models.user import User
from schemas.token import RefreshCreate, AccessEncode

TTL = int(os.getenv("REFRESH_EXPIRE_DAYS", 7)) * 24 * 60 * 60

class UserService:

    def __init__(self, uow: UnitOfWork, ramStorage: RamStorage):
        self.uow = uow
        self.ramStorage = ramStorage

    async def get_user(self, id: int) -> User|None:
        return await self.uow.users.get_user_by_id(id)
    
    async def get_user_by_username(self, username: str) -> User|None:
        return await self.uow.users.get_user_by_username(username)
    
    async def create_user(self, data: UserCreate) -> User|None:
        async with self.uow:
            data.password = password_helper.hash_password(data.password)
            return await self.uow.users.create_user(data)
    
    async def login_user(self, request: Request, response: Response, data: UserLogin) -> UserLoginResponce:
        async with self.uow:
            user = await self.get_user_by_username(data.username)

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User does not exist"
                )
            res = password_helper.verify_password(data.password, user.password)
            if not res:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Wrong credentials"
                )
            access = await self.set_tokens(response, user.id)
            return UserLoginResponce.model_validate({"user":user, "access_token": access})
        
    async def refresh_token(self, responce: Response, request: Request) -> str:
        async with self.uow:
            token = cookie.get_cookie(request)
            if not token:
                raise HTTPException(status_code=401, detail="no refresh token")
            
            token_hash = auth.hash_token(token)
            token_model = await self.uow.refresh_tokens.get_token_by_hash(token_hash)
            if not token_model:
                raise HTTPException(status_code=401, detail="no refresh token")
            
            if token_model.expires_at <= datetime.now(timezone.utc):
                raise HTTPException(status_code=401, detail="refresh token expired")

            if token_model.revoked:
                raise HTTPException(status_code=401, detail="refresh token revoked")
            
            try:
                await self.ramStorage.contains(token_model.user_id, token_model.sid, TTL)
            except:
                raise HTTPException(status_code=500, detail="ramstorage error")
            token_model.revoked = True
            token_model.revoked_at = datetime.now(timezone.utc)

            return {"access_token":await self.set_tokens(responce, token_model.user_id, token_model.sid)}

    
    async def logout_user(self, response:Response, request: Request) -> dict:
        async with self.uow:
            token = cookie.get_cookie(request)
            if token:
                token_hash = auth.hash_token(token)
                token_model = await self.uow.refresh_tokens.get_token_by_hash(token_hash)
                token_model.revoked = True
                await self.ramStorage.remove(token_model.user_id, token_model.sid)
            cookie.delete_cookie(response)
            
            return {"message" : "success"}
    
    async def set_tokens(self, response: Response,
                         user_id: int | None = None,
                         sid: str | None = None ) -> str:
        
              
        token_info = auth.create_refresh_token(user_id, sid, device_name=None)  
        refresh = token_info["token"] 
        refresh_schema = RefreshCreate.model_validate(token_info)
        to_encode = AccessEncode.model_validate(token_info)
        access = auth.create_access_token(to_encode.model_dump())
        await self.uow.refresh_tokens.create_token(refresh_schema)
        cookie.set_cookie(response, refresh)
        await self.ramStorage.add(user_id, refresh_schema.sid, TTL)
        return access