import asyncio
import datetime as dt
from os import environ
from pathlib import Path
from ping3 import ping
from ping3.errors import PingError

import tortoise
from tortoise import Tortoise

from ntmn.models import Ping

# env settings
FILE_PATH = environ.get(
    "FILE_PATH",
    default=f"{Path(__file__).parent.parent.parent / Path('.db')}",
)
DATABASE_URL = environ.get(
    "DATABASE_URL",
    default=f"sqlite:///{FILE_PATH}/{dt.datetime.now().isoformat()}.sqlite3",
)
PING_TARGET = environ.get(
    "PING_TARGET",
    default="us-digitalocean-sanfrancisco-01-1g.nperf.net",
)
INTERFACE = environ.get("INTERFACE", default="eth0")
TIMEOUT = int(environ.get("TIMEOUT", default="4"))
SLEEP = int(environ.get("SLEEP", default="10"))


async def ping_target(
    host: str,
    interface: str = INTERFACE,
    timeout: int = TIMEOUT,
) -> tuple[dt.datetime, float | None, str]:
    """ping target and return timestamp, latency, and status"""
    timestamp = dt.datetime.now(dt.timezone.utc)
    try:
        latency = ping(host, interface=interface, timeout=timeout, unit="ms")
        if latency is None:
            return timestamp, None, f"Disconnected (timeout={timeout}s)"
        return timestamp, latency, "Connected"
    except PingError as e:
        return timestamp, None, f"Error: {str(e)}"


async def main() -> None:
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["ntmn.models"]},
    )
    await Tortoise.generate_schemas()

    # ping the target and save the result
    while True:
        timestamp, latency, status = await ping_target(PING_TARGET)
        latency_str = f"{latency}ms" if latency is not None else "N/A"
        print(f"{timestamp}: {latency_str}, {status}")
        await Ping.create(timestamp=timestamp, latency=latency, status=status)
        await asyncio.sleep(SLEEP)


if __name__ == "__main__":
    try:
        tortoise.run_async(main())
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Quitting...")
