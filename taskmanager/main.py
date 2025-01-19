from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.responses import RedirectResponse

from taskmanager.core.config import settings

from taskmanager.api.v1.base_router import api_router


def include_middlewares(app):
    app.add_middleware(GZipMiddleware, minimum_size=1000)  # Add GZipMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )  # TODO - restrict origins
    app.add_middleware(SessionMiddleware, secret_key="some-random-string") # TODO - change secret key & move to env variable

    return app

def include_routers(app):
    app.include_router(api_router)
    return app


def start_api():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    app = include_middlewares(app)
    app = include_routers(app)
    return app

api = start_api()

# redirect / to /docs
@api.get("/")
async def redirect_to_docs():
    # TODO create a welcome page
    return RedirectResponse(url="/docs")
