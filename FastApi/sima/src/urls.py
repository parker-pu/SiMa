# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

路由
"""
from fastapi import APIRouter, FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html

router = APIRouter(responses={404: {"description": "Not found"}}, )

app = FastAPI()


@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        # openapi_url=app.openapi_url,
        openapi_url="/openapi.json",
        title="Swagger UI",
        # oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        oauth2_redirect_url="/docs/oauth2-redirect",
        swagger_js_url="/static/swagger/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger/swagger-ui.css",
        swagger_favicon_url="/static/swagger/favicon.png",
    )


@router.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        # openapi_url=app.openapi_url,
        openapi_url="/openapi.json",
        title="ReDoc",
        redoc_js_url="/static/redoc/redoc.standalone.js",
        redoc_favicon_url="/static/redoc/favicon.png",
    )
