from typing import Optional
from fastapi import (
    Request,
    Cookie,
    Depends
)
import jwt
from decouple import config
from models.item import ItemDocument


async def is_authenticated(request: Request, token: Optional[str] = Cookie(None, alias='jwt')):
    # Use alias to not overwrite built-in jwt module
    if not token or token is None:
        request.state.is_authenticated = False
    else:
        request.state.is_authenticated = True
    return request.state.is_authenticated


async def current_user(request: Request, token: Optional[str] = Cookie(None, alias='jwt'), is_authenticated=Depends(is_authenticated)):
    # Use alias to not overwrite built-in jwt module
    if not is_authenticated:
        request.state.current_user = None
        return None
    user = jwt.decode(token, config('JWT_KEY'))
    request.state.current_user = user
    return request.state.current_user
