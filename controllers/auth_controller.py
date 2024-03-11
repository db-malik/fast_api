from fastapi import HTTPException
from jose import JWTError

from utils.auth_utils import generate_salt, hash_password, verify_password
from middlewares.auth_middleware import create_access_token
from database.db_config import get_database_connection
from models.user_model import User

def register_user(name: str, email: str, password: str):
    try:
        # Generate a random salt
        salt = generate_salt()

        # Hash the password
        hashed_password = hash_password(password, salt)

        # Get a database connection
        connection = get_database_connection()
        cursor = connection.cursor()

        # Insert the new user into the database
        query = "INSERT INTO users (name, email, password, salt) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, hashed_password, salt))

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return {"message": "User registered successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {e}")

def login_user(email: str, password: str):
    try:
        # Get a database connection
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch the user from the database based on the email
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        if user and verify_password(password, user['password']):
            # Generate JWT token for the user
            token_data = {"sub": user['email']}
            token = create_access_token(token_data)
            return {"access_token": token, "token_type": "bearer"}

        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging in: {e}")
