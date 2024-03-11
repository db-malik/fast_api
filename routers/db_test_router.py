# db_test_router.py

from fastapi import APIRouter, Depends, HTTPException
from database.db_config import get_database_connection, close_database_connection

test_db_router = APIRouter()

@test_db_router.get("/test_db_connection")
async def test_db_connection():
    try:
        # This is just a test to check if the database connection works
        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        # If the query is successful, print a success message
        print("Successfully connected to the database!")

        # Close the cursor and connection
        cursor.close()
        close_database_connection(connection)

        return {"message": "Database connection successful!"}
    except Exception as e:
        # If there's an error, raise an HTTPException
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
