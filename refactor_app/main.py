import uuid
from typing import Annotated, Optional

from api.main import fetch_data
from fastapi import Cookie, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="./refactor_app/static"),
    name="static",
)


templates = Jinja2Templates(directory="./refactor_app/templates")

sessions = {}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


@app.post("/")
def data_fetcher(username: Annotated[str, Form()]):
    dfs, anilist_id, insights = fetch_data(username)
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"insights": insights}
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="session_id", value=session_id)
    return response


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, session_id: Optional[str] = Cookie(None)):
    if session_id not in sessions:
        raise HTTPException(status_code=403, detail="Invalid session")

    return templates.TemplateResponse(
        request=request, name="dashboard.html", context=sessions[session_id]["insights"]
    )
