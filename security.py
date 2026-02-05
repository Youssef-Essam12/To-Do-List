import bcrypt
import hashlib
from fastapi import Request
from sqlalchemy.orm import Session
import secrets
import redis
from models import User

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


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
    accept_header = request.headers.get("Content-Type", "")
    is_api_request = "application/json" in accept_header
    if (is_api_request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        session_id = auth_header.split(" ")[1]
    else:
        session_id = request.cookies.get("session_id")
    if not session_id:
        return None
    
    user_id = redis_client.get(f"session_id:{session_id}")
    if not user_id:
        return None
    
    return db.query(User).get(int(user_id))

def logout(session_id):
    redis_client.delete(f"session_id:{session_id}")