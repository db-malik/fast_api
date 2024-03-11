
from database.db_config import get_database_connection, close_database_connection
from fastapi import HTTPException

from utils.auth_utils import hash_password, verify_password, generate_salt

def get_all_users():
    try:
        # Get a database connection
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        # Execute a raw SQL query to fetch all users
        query = "SELECT * FROM users"
        cursor.execute(query)

        # Fetch all the results
        users = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        close_database_connection(connection)

        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {e}")



def get_user_by_id(user_id: int):
    try:
        # Get a database connection
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        # Execute a raw SQL query to fetch a user by ID
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))

        # Fetch the result
        user = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        close_database_connection(connection)

        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {e}")
      

      
      
def create_user(name: str, email: str, password: str):
    try:
        # Get a database connection
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Generate a random salt
        salt = generate_salt()
        # Hash the password
        hashed_password = hash_password(password, salt)
        
        
        
        # Execute a raw SQL query to insert a new user
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, hashed_password))

        # Commit the transaction
        connection.commit()

        # Fetch the ID of the newly created user
        new_user_id = cursor.lastrowid

        # Close the cursor and connection
        cursor.close()
        close_database_connection(connection)

        # Return the created user
        return {"id": new_user_id, "name": name, "email": email}

    except Exception as e:
        # Rollback the transaction in case of an error
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating user: {e}")
      
    

def get_user_by_username(username: str):
    try:
        # Get a database connection
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        # Execute a raw SQL query to fetch a user by username
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))

        # Fetch the result
        user_data = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        close_database_connection(connection)

        if user_data:
            # Assuming your User model has an initialization method
            return User(**user_data)
        else:
            return None  # User not found

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user by username: {e}")


def get_user_by_email(email: str):
    try:
        # Get a database connection
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        # Execute a raw SQL query to fetch a user by email
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))

        # Fetch the result
        user_data = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        close_database_connection(connection)

        if user_data:
            # Assuming your User model has an initialization method
            return User(**user_data)
        else:
            return None  # User not found

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user by email: {e}")