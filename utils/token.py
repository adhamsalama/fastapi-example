import jwt
from models.user import User, UserIn
from decouple import config


def generate_jwt(user: User):
    token = jwt.encode(payload={'email': user.email, 'id': str(user.id)},
                       key=config('JWT_KEY')).decode()
    return token
