# auth_utils.py

import os
import uuid
import hashlib
from jose import JWTError, jwt

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

def generate_salt():
    """
    Generate a random salt for password hashing.
    """
    salt = uuid.uuid4().hex
    return salt

def hash_password(password, salt):
    """
    Hash the password using sha256 with a random salt.
    """
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def verify_password(plain_password, hashed_password):
    """
    Verify if the plain password matches the hashed password.
    """
    try:
        hashed_password, salt = hashed_password.split(':')
        return hashed_password == hashlib.sha256(salt.encode() + plain_password.encode()).hexdigest()
    except ValueError:
        return False