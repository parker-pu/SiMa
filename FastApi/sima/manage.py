# -*- coding: utf-8 -*-
import os
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Depends
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from src.apps.dynamic_api.urls import router as dynamic_api_router
from src.apps.token.urls import router as token_router
from src.apps.user.urls import router as user_router
from src.apps.databases.urls import router as db_router
from src.apps.dictionary.urls import router as dictionary_router

from src.apps.user.views import get_current_active_user
from src.schedule import add_schedule
from src.settings import HOST, PORT, LOG_LEVEL, MIDDLEWARE, DEBUG, RELOAD, BASE_DIR

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from src.urls import router

scheduler = AsyncIOScheduler()
app = FastAPI(
    title="SiMa",
    description="Data Dictionary",
    version="2023.12",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# ADD middleware
for middleware_name, middleware_data in MIDDLEWARE.items():
    app.add_middleware(middleware_name, **middleware_data)

# ADD URL
app.include_router(router)
app.include_router(token_router, prefix="/api")
app.include_router(dynamic_api_router, prefix="/api", dependencies=[Depends(get_current_active_user)])
app.include_router(user_router, prefix="/api", dependencies=[Depends(get_current_active_user)])
app.include_router(db_router, prefix="/api", dependencies=[Depends(get_current_active_user)])
app.include_router(dictionary_router, prefix="/api", dependencies=[Depends(get_current_active_user)])

# app.include_router(apps.first.router, prefix="/api")
# app.include_router(apps.dashboard.router, prefix="/api", dependencies=[Depends(get_current_active_user)])
# app.include_router(apps.comment.router, prefix="/api", dependencies=[Depends(get_current_active_user)])


@app.get("/")
async def get_index():
    return FileResponse('static/index.html')


@app.get("/{whatever:path}")
async def get_static_files_or_404(whatever):
    # try open file for path
    file_path = os.path.join("static", whatever)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse('static/index.html')


@app.on_event("startup")
def init_scheduler():
    """ setup start """
    FastAPICache.init(InMemoryBackend(), prefix="cache_key")
    # add_schedule(scheduler)
    # scheduler.start()


if __name__ == '__main__':
    uvicorn.run(
        "manage:app",
        host=HOST,
        port=PORT,
        log_level=LOG_LEVEL,
        reload=RELOAD,
        reload_dirs=[f"{BASE_DIR}/reload"],
        use_colors=True,
        forwarded_allow_ips="*",
    )
