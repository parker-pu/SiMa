# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from starlette import status
from src.apps.user.models import TokenDataModel, UserModel, UserInDBMode, InitEsConnModel
from src.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.utils.log import logger
from src.utils.passwd import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/token")


def get_user(username: str):
    u = UserInDBMode(username=username)
    u.load()
    return u


def authenticate_user(username: str, password: str):
    """ authenticate user """
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
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


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataModel(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def gen_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Login to get access Token

    :param form_data: input data
    :return:
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def init_superuser(init_data: InitEsConnModel, user: UserInDBMode):
    revoke_data: dict = {
        "es_conn": False,
        "add_user": False
    }
    try:
        if init_data.conn().ping() and not init_data.save():
            revoke_data["es_conn"] = True

        if not user.create_index() and not user.save():
            revoke_data["add_user"] = True

        if len(revoke_data.values()) != sum(revoke_data.values()):
            init_data.delete()
    except Exception as e:
        logger.info(e)
    return revoke_data
