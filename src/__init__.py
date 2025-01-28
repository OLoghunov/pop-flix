from fastapi import FastAPI
from .search.routes import searchRouter
from .auth.routes import authRouter
from .middleware import registerMiddleware
from .errors import registerAllErrors

app = FastAPI()

version = "0.1"

app = FastAPI(
    title="Movie service",
    description="A REST API for online movie service",
    version=version,
)

registerAllErrors(app)

registerMiddleware(app)

app.include_router(searchRouter, prefix="/api/{version}/search", tags=["search"])
app.include_router(authRouter, prefix="/api/{version}/auth", tags=["auth"])