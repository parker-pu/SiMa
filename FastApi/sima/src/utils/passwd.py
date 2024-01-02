# -*- coding: utf-8 -*-
import base64

from cryptography.fernet import Fernet
from passlib.context import CryptContext

from src.settings import SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
cipher_suite = Fernet(base64.urlsafe_b64encode(SECRET_KEY.encode()[:32]))  # 用于加解密


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


def encrypted_text(text: str) -> str:
    """
    加密 text 文本
    :param text:
    :return:
    """
    return cipher_suite.encrypt(text.encode()).decode()


def decrypted_text(text: str) -> str:
    """
    解密 text 文本
    :param text:
    :return:
    """
    return cipher_suite.decrypt(text).decode()
