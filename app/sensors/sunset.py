"""Outdoor brightness sensor using sunrise-sunset.org API."""

import json
import urllib.request

from datetime import datetime, timezone
from pathlib import Path


CONFIG_PATH = Path(__file__).parent / "sunset-config.json"


def _load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def _sunset_url(config):

    location_name = config["current_location"]

    location = config["locations"][location_name]

    return (
        "https://api.sunrise-sunset.org/json"
        f"?lat={location['latitude']}"
        f"&lng={location['longitude']}"
        "&formatted=0"
    )


def sun_has_set() -> bool | None:
    """
    Return True if the sun has set.
    Return False if the sun is still up.
    Return None if the check failed.
    """

    config = _load_config()

    # -------------------------
    # Debug override
    # -------------------------

    override = config.get("debug_override")

    if override == "day":
        return False

    if override == "night":
        return True


    # -------------------------
    # Real API lookup
    # -------------------------

    try:
        req = urllib.request.Request(
            _sunset_url(config),
            headers={
                "User-Agent": "Goods-Stay-Good/1.0"
            },
        )

        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(
                resp.read().decode()
            )

        if data.get("status") != "OK":
            return None

        sunset = datetime.fromisoformat(
            data["results"]["sunset"]
        ).timestamp()

        now = datetime.now(
            timezone.utc
        ).timestamp()

        return now >= sunset

    except Exception as e:
        print(f"Sunset lookup failed: {e}")
        return None
