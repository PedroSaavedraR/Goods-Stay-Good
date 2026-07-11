from pathlib import Path
from datetime import datetime


LOG_FILE = (
    Path(__file__).parent.parent
    / "log"
    / "events.log"
)


def reset():

    LOG_FILE.parent.mkdir(
        exist_ok=True
    )


    LOG_FILE.write_text(
        "=== Smart Truck Log Started ===\n"
    )



def log(message):

    LOG_FILE.parent.mkdir(
        exist_ok=True
    )


    timestamp = datetime.now().isoformat(
        timespec="seconds"
    )


    line = (
        f"{timestamp} | {message}\n"
    )


    with LOG_FILE.open("a") as file:

        file.write(line)


    print(f"[LOG] {message}")
