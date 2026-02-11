import bcrypt
import hashlib
from fastapi import Request
from sqlalchemy.orm import Session
import secrets
import redis
from models import User
from dotenv import load_dotenv
import os

load_dotenv()

redis_client = redis.Redis.from_url(os.environ["REDIS_URL"])


def _pre_hash(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).hexdigest().encode("utf-8")

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(_pre_hash(password), salt)
    return hashed.decode("utf-8")

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(_pre_hash(password), password_hash.encode("utf-8"))

def generate_session_id():
    return secrets.token_urlsafe(32)

# returns User object of the current logged in user
def get_logged_user(request: Request, db: Session):
    session_id = ""
    auth_header = request.headers.get("Authorization")
    is_api = auth_header and auth_header.startswith("Bearer ")
    if is_api:
        session_id = auth_header.split(" ")[1]
    else:
        session_id = request.cookies.get("session_id")
    if not session_id:
        return (None, is_api)
    
    user_id = redis_client.get(f"session_id:{session_id}")
    if not user_id:
        return (None, is_api)
    
    return (db.query(User).get(int(user_id)), is_api)

def logout(session_id):
    redis_client.delete(f"session_id:{session_id}")