# Core FastAPI application
from fastapi import FastAPI

# Middlewares
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# Core
from taskmanager.core.config import settings


def include_middlewares(app):
    app.add_middleware(GZipMiddleware, minimum_size=1000)  # Add GZipMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )  # TODO - restrict origins
    app.add_middleware(SessionMiddleware, secret_key="some-random-string")

    return app


def start_api():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    app = include_middlewares(app)
    return app

api = start_api()
