# db_config.py

from dotenv import load_dotenv
import os
import mysql.connector
from fastapi import HTTPException

# Load environment variables from .env file
load_dotenv()

HOST = os.getenv("HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
PORT_NUMBER = os.getenv("PORT_NUMBER")

def get_database_connection():
    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(
            host=HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME,
            port=PORT_NUMBER
        )
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error establishing database connection: {e}")

def close_database_connection(connection):
    try:
        if connection.is_connected():
            connection.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error closing database connection: {e}")
