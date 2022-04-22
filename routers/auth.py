from models.user import User, UserIn
from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    Response,
    Depends
)
from dependencies import current_user

from utils.token import generate_jwt
from utils.hash_password import hash_password

router = APIRouter(prefix='/auth')


@router.post('/register', response_model=User, response_model_exclude={'password'})
async def register(user_info: UserIn, response: Response):
    existing_user = await User.find_one({'email': user_info.email})
    if existing_user:
        raise HTTPException(status_code=400, detail={
                            'message': 'Email already taken'})
    hashed_password = hash_password(user_info.password)
    user = User(email=user_info.email, password=hashed_password)
    await user.insert()
    token = generate_jwt(user)
    response.set_cookie('jwt', token)
    response.status_code = 201
    return user


@router.post('/login', response_model=User, response_model_exclude={'password'})
async def login(user_info: UserIn, response: Response):
    user = await User.find_one({'email': user_info.email})
    if user is None:
        raise HTTPException(status_code=404, detail={
                            'message': 'User not found'})
    token = generate_jwt(user)
    response.set_cookie('jwt', token)
    return user


@router.post('/logout')
def logout(request: Request, response: Response):
    response.delete_cookie('jwt')


@router.get('/current-user')
def get_current_user(_current_user=Depends(current_user)):
    return _current_user
