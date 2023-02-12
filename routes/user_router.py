
from fastapi import APIRouter

from fastapi.responses import HTMLResponse
from utils.jwt_manager import create_token
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from schemas.user_schemas import User
user_router=APIRouter()

# Login user
@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)