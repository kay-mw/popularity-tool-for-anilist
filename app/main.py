import json
import sqlite3
import uuid
from typing import Annotated, Optional

from api.anime.main import fetch_anime
from api.manga.main import fetch_manga
from database import init_db
from fastapi import Cookie, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="./app/static"),
    name="static",
)


templates = Jinja2Templates(directory="./app/templates")

DATABASE_NAME = "sessions.db"

init_db(DATABASE_NAME)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


@app.post("/")
def data_fetcher(username: Annotated[str, Form()], manga: bool = Form(False)):
    if not manga:
        try:
            dfs, anilist_id, insights = fetch_anime(username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
    else:
        try:
            dfs, anilist_id, insights = fetch_manga(username)
            insights["manga"] = manga
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    session_id = str(uuid.uuid4())

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (session_id, insights) VALUES (?, ?)",
        (session_id, json.dumps(insights)),
    )
    conn.commit()
    conn.close()

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="session_id", value=session_id)
    return response


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, session_id: Optional[str] = Cookie(None)):
    if not session_id:
        raise HTTPException(
            status_code=403,
            detail="Invalid session.",
        )

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT insights FROM sessions WHERE session_id = ?", (session_id,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        raise HTTPException(
            status_code=403,
            detail="Invalid session. Could not find any user insights data.",
        )

    insights = json.loads(result[0])

    return templates.TemplateResponse(
        request=request, name="dashboard.html", context=insights
    )
