# main.py
import sys
import os
from fastapi import FastAPI, Depends,  HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from controllers.auth_controller import login_user
from database.db_config import  get_database_connection, close_database_connection

from routers.home_router import home_router
from routers.user_router import user_router
from routers.ml_model_router import ml_model_router
from routers.db_test_router import test_db_router

app = FastAPI()


# CORS middleware for handling cross-origin resource sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routers here

app.include_router(home_router, prefix="", tags=[""])
app.include_router(test_db_router, prefix="/test_database", tags=["test"])  

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(ml_model_router, prefix="/models", tags=["models"])


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        # Call the login_user function to authenticate the user
        token = login_user(form_data.username, form_data.password)
        
        # Return the token as the response
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException as e:
        # If authentication fails, raise the exception to let FastAPI handle the HTTP response
        raise e