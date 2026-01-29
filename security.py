from passlib.context import CryptContext
pwd_mngr = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    return pwd_mngr.hash(password)

def verify_password(password, password_hash):
    return pwd_mngr.verify(password, password_hash)

