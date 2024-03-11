# user_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List  

from models.user_model import User 
from controllers.user_controller import get_all_users, get_user_by_id, create_user
from controllers.auth_controller import register_user, login_user

from middlewares.auth_middleware import   decode_access_token, authenticate_user

user_router = APIRouter()

# Public route to create a new user
@user_router.post("/users", response_model=dict)
async def create_new_user(name: str, email: str, password: str):
    return create_user(name, email, password)


# Public Route for user login
@user_router.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    try:
        # Call the login_user function
        return login_user(email, password)
    except HTTPException as e:
        raise e  # Re-raise the exception to let FastAPI handle the HTTP response


# Private route to get all users (requires authentication)
@user_router.get("/users", response_model=list[dict])
async def get_users(current_user: dict = Depends(authenticate_user)):
    return get_all_users()


# Private route to get a user by ID (requires authentication)
@user_router.get("/users/{user_id}", response_model=dict)
async def get_user(user_id: int, current_user: dict = Depends(authenticate_user)):
    return get_user_by_id(user_id)




# Private route that requires authentication
@user_router.get("/private")
async def private_route(current_user: dict = Depends(login_user)):
    return {"message": "This is a private route", "current_user": current_user}


