# routers/home_router.py

from fastapi import APIRouter

home_router = APIRouter()

@home_router.get("/")
async def read_home():
    return {"message": "Welcome to the API home page!"}
