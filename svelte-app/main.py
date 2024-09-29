from contextlib import asynccontextmanager

from api.anime.main import fetch_anime
from api.manga.main import fetch_manga
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend())
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/home/")
@cache(expire=86400)
def process_preferences(username: str, manga: bool):
    if 2 < len(username) < 20:
        if manga:
            _, _, insights = fetch_manga(username)
            return {"insights": insights}
        else:
            _, _, insights = fetch_anime(username)
            return {"insights": insights}
