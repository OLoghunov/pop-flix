from fastapi import FastAPI
from .search.routes import searchRouter

app = FastAPI()

version = "0.1"

app = FastAPI(
    title="Movie service",
    description="A REST API for online movie service",
    version=version,
)

# registerAllErrors(app)

app.include_router(searchRouter, prefix="/api/{version}/search", tags=["search"])