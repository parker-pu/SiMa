# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from src.apps.user.models import UserModel
from src.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.utils.db.aiodb import get_db_session
from src.utils.passwd import verify_password

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)


async def get_user(db_session, username: str) -> UserModel:
    result = await db_session.execute(select(UserModel).where(UserModel.username == username))
    u: UserModel = result.scalars().one()
    return u


async def authenticate_user(db_session, username: str, password: str):
    """ authenticate user """
    user = await get_user(db_session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def gen_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db_session=None):
    """ Login to get access Token

    :param form_data: input data
    :param db_session:
    :return:
    """
    user = await authenticate_user(db_session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
