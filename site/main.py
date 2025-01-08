from contextlib import asynccontextmanager

from api.main import fetch_data
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from requests.exceptions import HTTPError


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend())
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # "https://www.anipop.uk",  # Prod
        # "https://anipop.uk",  # Prod
        "http://localhost:5173",  # Dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/home/")
@cache(expire=3600)
def process_preferences(username: str, manga: bool):
    if 2 < len(username) < 20:
        try:
            _, _, insights = (
                fetch_data(username=username, format="manga")
                if manga
                else fetch_data(username=username, format="anime")
            )
            return {"insights": insights}
        except ValueError or HTTPError as e:
            raise HTTPException(status_code=404, detail=f"{e}")
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Username '{username}' has an invalid length (<2 or >20 characters).",
        )
