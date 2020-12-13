# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI, Depends
from starlette.staticfiles import StaticFiles

from src import apps
from src.apps.user.views import get_current_active_user
from src.settings import HOST, PORT, LOG_LEVEL, MIDDLEWARE, DEBUG, RELOAD

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
app.include_router(apps.user.router)
app.include_router(apps.dictionary.router, dependencies=[Depends(get_current_active_user)])

if __name__ == '__main__':
    uvicorn.run(
        "manage:app",
        host=HOST,
        port=PORT,
        log_level=LOG_LEVEL,
        debug=DEBUG,
        reload=RELOAD,
    )
