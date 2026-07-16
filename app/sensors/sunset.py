"""Outdoor brightness sensor using sunrise-sunset.org API for Germany."""
import time
import json
import urllib.request
import urllib.error
import threading
from datetime import datetime, timezone

from config import CONFIG
from logger import log


SUNSET_URL = (
    f"https://api.sunrise-sunset.org/json"
    f"?lat={CONFIG.sunset_lat}&lng={CONFIG.sunset_lng}&formatted=0"
)


class SunsetChecker:
    """Fetches sunset time once and caches per day; thread-safe."""

    def __init__(self):
        self._sunset_utc: float | None = None
        self._sunrise_utc: float | None = None
        self._fetch_date: str | None = None
        self._lock = threading.Lock()
        self._refetch()

    def _refetch(self):
        """Fetch today's sunset/sunrise times from the API."""
        try:
            req = urllib.request.Request(SUNSET_URL, headers={"User-Agent": "Goods-Stay-Good/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
            if data.get("status") != "OK":
                log.warning("Sunset API returned non-OK status")
                return

            results = data["results"]
            # Parse ISO 8601 timestamps
            self._sunrise_utc = datetime.fromisoformat(
                results["sunrise"]
            ).timestamp()
            self._sunset_utc = datetime.fromisoformat(
                results["sunset"]
            ).timestamp()
            self._fetch_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            log.info(
                "Sunset times: sunrise %s, sunset %s",
                results["sunrise"],
                results["sunset"],
            )
        except (urllib.error.URLError, json.JSONDecodeError, KeyError) as exc:
            log.error("Failed to fetch sunset data: %s", exc)

    def sun_has_set(self) -> bool | None:
        """Return whether the sun has set (True/False), or None if unknown."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        # Refetch once per day
        if today != self._fetch_date:
            self._refetch()

        if self._sunset_utc is None or self._sunrise_utc is None:
            return None

        now = time.time()
        # Between sunrise and sunset = daylight
        if self._sunrise_utc <= now < self._sunset_utc:
            return False
        else:
            return True


sunset_checker = SunsetChecker()
