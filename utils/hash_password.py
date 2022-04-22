import bcrypt

from decouple import config


def hash_password(password: str) -> str:
    """Returns a salted password hash"""
    return bcrypt.hashpw(password.encode(),
                         bcrypt.gensalt()).decode()
