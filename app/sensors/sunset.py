"""Outdoor brightness sensor using sunrise-sunset.org API for Berlin."""

import urllib.request
import json
from datetime import datetime, timezone


SUNSET_URL = (
    "https://api.sunrise-sunset.org/json"
    "?lat=52.5200&lng=13.4050&formatted=0"
)


def sun_has_set() -> bool | None:
    """Return True if the sun has set in Berlin, False otherwise."""
    try:
        req = urllib.request.Request(
            SUNSET_URL,
            headers={"User-Agent": "Goods-Stay-Good/1.0"},
        )

        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())

        if data.get("status") != "OK":
            return None

        sunset = datetime.fromisoformat(
            data["results"]["sunset"]
        ).timestamp()

        return datetime.now(timezone.utc).timestamp() >= sunset

    except Exception:
        return None
