# -*- coding: utf-8 -*-
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import (
    SecurityScopes,
)

from src.apps.token.views import oauth2_scheme, get_user
from src.apps.user.models import UserModel
from src.apps.user.validate import TokenDataValidate
from src.settings import SECRET_KEY, ALGORITHM
from src.utils.db.aiodb import get_db_session


async def get_current_user(
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(oauth2_scheme),],
        db_session: AsyncSession = Depends(get_db_session)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenDataValidate(scopes=token_scopes, username=username)
    except JWTError:
        raise credentials_exception

    user = await get_user(db_session=db_session, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
        current_user: Annotated[UserModel, Security(get_current_user, scopes=["me"])]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
