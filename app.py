from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

from database import get_guild, get_or_create_guild, set_prefix

app = FastAPI()

# HTML Templates
templates = Jinja2Templates(directory=".")

# Static files (CSS)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def index(request: Request):
    # Beispiel: Liste aller Guilds holen
    # Wenn du eine Liste möchtest, musst du in der DB eine Guilds-Tabelle füllen
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/guild/{guild_id}")
async def guild_page(request: Request, guild_id: int):
    guild = get_or_create_guild(guild_id)
    return templates.TemplateResponse(
        "guild.html",
        {
            "request": request,
            "guild_id": guild[0],
            "prefix": guild[1]
        }
    )

@app.get("/guild/{guild_id}/set_prefix")
async def update_prefix(request: Request, guild_id: int, prefix: str):
    set_prefix(guild_id, prefix)
    guild = get_or_create_guild(guild_id)
    return templates.TemplateResponse(
        "guild.html",
        {
            "request": request,
            "guild_id": guild[0],
            "prefix": guild[1],
            "message": "Prefix updated!"
        }
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
