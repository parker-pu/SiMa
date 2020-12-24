# -*- coding: utf-8 -*-
"""
Use APSchedule
"""

from src.apps.dictionary.views import sync_data_view
from src.settings import SYNC_DATA_SECONDS


def add_schedule(scheduler):
    scheduler.add_job(sync_data_view, 'interval', seconds=SYNC_DATA_SECONDS)
