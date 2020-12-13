# -*- coding: utf-8 -*-
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """ Is the hash of the two values equal
    :param plain_password: plaintext
    :param hashed_password: hash password
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def gen_password_hash(data):
    """ Generate password hash
    :param data: plaintext data
    :return:
    """
    return pwd_context.hash(data)
