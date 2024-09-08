from api.anime.main import fetch_anime
from api.manga.main import fetch_manga
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserPreferences(BaseModel):
    manga_checked: bool
    username: str


@app.post("/api/home")
def process_preferences(prefs: UserPreferences):
    try:
        if prefs.manga_checked:
            _, _, insights = fetch_manga(prefs.username)
            return {"insights": insights}
        else:
            _, _, insights = fetch_anime(prefs.username)
            return {"insights": insights}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
