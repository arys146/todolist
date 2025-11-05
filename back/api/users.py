from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from services.user import UserService
from repo.provider import provide_user_service
from models.user import User
from middleware.auth import get_current_user_oauth2
from schemas.user import UserCreate, UserLoginResponce, UserRead, UserLogin
from schemas.token import RefreshResponce

def user_routes() -> APIRouter:
    router = APIRouter()
    
    @router.post("/user", response_model=UserRead)
    async def create_user(data: UserCreate, service: UserService = Depends(provide_user_service)):
        return await service.create_user(data)
    
    @router.post("/login", response_model=UserLoginResponce)
    async def login_user(data: UserLogin, response: Response, request: Request, service: UserService = Depends(provide_user_service)):
            return await service.login_user(request, response, data)
    
    @router.post("/login-form", response_model=UserLoginResponce)
    async def login_user_with_form(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, request: Request, service: UserService = Depends(provide_user_service)):
        try:
                data = UserLogin(username=form_data.username, password=form_data.password)
        except ValidationError as e:
                raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=f"Invalid input: {e.errors()}",
                )

        return await service.login_user(request, response, data)
    
    @router.post("/check-auth")
    async def check_auth(user: User = Depends(get_current_user_oauth2)):
            return {"Success"}
    
    @router.post("/auth/refresh", response_model=RefreshResponce)
    async def refresh_token(response: Response, request: Request, service: UserService = Depends(provide_user_service)):
        return await service.refresh_token(response, request)
    
    @router.post("/auth/logout")
    async def logout_user(response: Response, request: Request, service: UserService = Depends(provide_user_service)):
            return await service.logout_user(response, request)

    
    return router