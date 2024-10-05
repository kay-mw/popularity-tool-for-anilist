from contextlib import asynccontextmanager

from api.anime.main import fetch_anime
from api.manga.main import fetch_manga
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
        "https://www.anipop.uk",
        "https://anipop.uk",
        # "http://localhost:5173", # Dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/home/")
@cache(expire=86400)
def process_preferences(username: str, manga: bool):
    if 2 < len(username) < 20:
        if manga:
            try:
                _, _, insights = fetch_manga(username)
                return {"insights": insights}
            except ValueError as e:
                raise HTTPException(status_code=404, detail=f"{e}")
            except HTTPError as e:
                raise HTTPException(status_code=404, detail=f"{e}")
        else:
            try:
                _, _, insights = fetch_anime(username)
                return {"insights": insights}
            except ValueError as e:
                raise HTTPException(status_code=404, detail=f"{e}")
            except HTTPError as e:
                raise HTTPException(status_code=404, detail=f"{e}")
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Username '{username}' has an invalid length (<2 or >20 characters).",
        )
