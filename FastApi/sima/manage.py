# -*- coding: utf-8 -*-

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Depends
from starlette.staticfiles import StaticFiles

from src import apps
from src.apps.user.views import get_current_active_user
from src.schedule import add_schedule
from src.settings import HOST, PORT, LOG_LEVEL, MIDDLEWARE, DEBUG, RELOAD

scheduler = AsyncIOScheduler()
app = FastAPI(
    title="SiMa",
    description="Data Dictionary",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# ADD middleware
for middleware_name, middleware_data in MIDDLEWARE.items():
    app.add_middleware(middleware_name, **middleware_data)

# ADD URL
app.include_router(apps.user.router, prefix="/api")
app.include_router(apps.dictionary.router, prefix="/api", dependencies=[Depends(get_current_active_user)])
app.include_router(apps.comment.router, prefix="/api", dependencies=[Depends(get_current_active_user)])


@app.on_event('startup')
def init_scheduler():
    """ setup start """
    add_schedule(scheduler)
    scheduler.start()


if __name__ == '__main__':
    uvicorn.run(
        "manage:app",
        host=HOST,
        port=PORT,
        log_level=LOG_LEVEL,
        debug=DEBUG,
        reload=RELOAD,
    )
