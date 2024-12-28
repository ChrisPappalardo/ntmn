# import datetime as dt
# from dateutil.relativedelta import relativedelta
# from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from ntmn import __version__
from ntmn.core import DATABASE_URL
from ntmn.models import (
    Ping,
    PingPydantic,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["ntmn.models"]},
    add_exception_handlers=True,
)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "ntmn", "version": f"{__version__}"}


@app.get("/pings/")
@app.get("/pings/{history}/")
async def pings_list(
    history: int = 100,
) -> list[PingPydantic]:  # type: ignore
    """list pings"""
    return await Ping.all().limit(history)


@app.get("/disconnects/")
@app.get("/disconnects/{history}/")
async def disconnects_list(
    history: int = 100,
) -> list[PingPydantic]:  # type: ignore
    return await Ping.filter(status__contains="Disconnected").limit(history)
