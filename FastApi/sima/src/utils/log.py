# -*- coding: utf-8 -*-
import os
import time

from loguru import logger

from src.settings import LOG_PATH, LOG_LEVEL

log_path = os.path.join(LOG_PATH, 'logs')

if not os.path.exists(log_path):
    os.mkdir(log_path)

log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}.log')
logger.add(log_path_error, rotation="12:00", retention="5 days", enqueue=True, level=LOG_LEVEL.upper())
