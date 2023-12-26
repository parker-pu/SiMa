# -*- coding: utf-8 -*-

import os
from starlette.middleware.cors import CORSMiddleware

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Token
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = 'wpdx&o!@(mt$xacf^p+o+3nn*h!y6_7x3%d=a0^go8b7_69dw6'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

ORIGINS = ["*"]

DEBUG = True
RELOAD = True

# db
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "123456"

# 缓存
CACHE_TIME = 10

CURRENT_VERSION = 2023.12  # 当前最新版本

# manage
HOST = "0.0.0.0"
PORT = 80

LOG_LEVEL = "info"
LOG_PATH = BASE_DIR

# conf
CONN_PATH = BASE_DIR + "/conn.json"

INSTALLED_APPS = []

# sync
SYNC_DATA_SECONDS = 3 * 60

# MIDDLEWARES
MIDDLEWARE = {
    CORSMiddleware: {
        "allow_origins": ORIGINS,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"]
    },
}

SUCCESS_DATA = {"status": 0, "message": "success"}
