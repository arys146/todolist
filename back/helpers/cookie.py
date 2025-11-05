from fastapi import Response, Request
import os


REFRESH_EXPIRE_DAYS = int(os.getenv("REFRESH_EXPIRE_DAYS", 7))
NAME = os.getenv("REFRESH_TOKEN_NAME", "refresh_token")

def set_cookie(response: Response, token: str):
    response.set_cookie(
            key=NAME,
            value=token,
            httponly=True,
            max_age=REFRESH_EXPIRE_DAYS * 24 * 60 * 60, 
            expires=REFRESH_EXPIRE_DAYS * 24 * 60 * 60,
            secure=False,           
            samesite="lax",
            path="/auth"
        )
    
def delete_cookie(response: Response):
    response.delete_cookie(NAME)

def get_cookie(request: Request):
    return request.cookies.get(NAME)