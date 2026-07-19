# File explanations

This file lists repository files and explains their purpose. Use this as a quick reference when navigating or extending the project.

---

## Root

- [README.md](README.md): Detailed project README (overview, architecture, setup, running, contributing).
- [LICENSE](LICENSE): MIT license for the project.
- [.gitignore](.gitignore): Files and folders excluded from version control and developer notes.

## app/

- [app/__init__.py](app/__init__.py): Package marker for the `app` package (empty).
- [app/main.py](app/main.py): Orchestrator and entry point. Runs the continuous sense → plan → act loop:
  - reads sensors via `sensors.sensor_reader.read()`
  - updates `WorldState`
  - generates a PDDL problem via `planner/problem_generator.py`
  - calls the planner through `planner_bridge.plan()`
  - executes planner actions via `executor.execute()`
  - handles graceful shutdown and initial actuator reset.
- [app/executor.py](app/executor.py): Maps planner action names to effects: updates `WorldState` (fan/heater booleans) and calls hardware through `hardware_manager` when required. Raises on unknown actions.
- [app/planner_bridge.py](app/planner_bridge.py): Subprocess wrapper that runs Fast Downward in `fast-downward/` to solve the generated PDDL problem (`planner/problem.pddl`). Parses the produced `sas_plan` and returns the next action or `None`.

## app/world_state/

- [app/world_state/world_state.py](app/world_state/world_state.py): Central world model and symbolic classification logic. Responsibilities:
  - loads runtime thresholds and other configuration from `config.json`
  - stores actuator flags (`fan_on`, `heater_on`) and symbolic sensor-derived state (`temperature`, `air_quality` enums)
  - exposes `update_from_sensors()` to convert raw sensor readings into symbolic states
  - exposes helper methods called by the executor (`fan_enabled()`, `heater_disabled()`, etc.)
- [app/world_state/config.json](app/world_state/config.json): Thresholds for classifying temperature and humidity (used by `WorldState`). Edit to tune behavior.

## app/hardware/

- [app/hardware/__init__.py](app/hardware/__init__.py): Package marker for the hardware module (empty).
- [app/hardware/hardware_manager.py](app/hardware/hardware_manager.py): High-level hardware API used across the app. Provides human-friendly functions such as `fan_on()`, `fan_off()`, `buzzer_on()` and delegates to concrete drivers in this folder.
- [app/hardware/relay.py](app/hardware/relay.py): I²C driver for a PCAL9535A-based relay board. It:
  - configures the IC ports as outputs via SMBus
  - maintains a byte bitmask of outputs (relays are active LOW)
  - exposes functions to toggle mapped relays (cargo LED, driving lights, fan, heating lamp).
- [app/hardware/buzzer.py](app/hardware/buzzer.py): PWM buzzer control using RPi.GPIO. Configures a GPIO pin and exposes `on()`/`off()` to start/stop PWM.

## app/sensors/

- [app/sensors/__init__.py](app/sensors/__init__.py): Package marker for sensors (empty).
- [app/sensors/sensor_reader.py](app/sensors/sensor_reader.py): Aggregator that produces a `SensorSnapshot` dataclass. It:
  - reads the thread-safe `mqtt_state.snapshot()` from `mqtt.py`
  - converts motion timestamps to Python datetimes
  - fetches ultrasonic distance via `ultrasonic.get_distance()`
  - queries `sunset.sun_has_set()` and bundles all values into the snapshot consumed by `WorldState`.
- [app/sensors/mqtt.py](app/sensors/mqtt.py): MQTT listener and in-memory state. Details:
  - connects to `localhost:1883` and subscribes to `zwave/#`
  - parses JSON payloads and updates `MQTTState` fields (`temperature`, `humidity`, `motion`, `motion_timestamp`) under a lock
  - starts the `paho-mqtt` loop in a background thread at import time so other scripts can simply import `mqtt_state` and use `snapshot()`.
- [app/sensors/ultrasonic.py](app/sensors/ultrasonic.py): HC-SR04 ultrasonic distance reader using RPi.GPIO. Sends trigger pulses, measures echo with timeouts, and returns distance in centimeters or `None` on timeout.
- [app/sensors/button.py](app/sensors/button.py): GPIO button handler using `gpiozero.Button` on pin 17. On press, logs a message and calls `world.acknowledge_cargo()` to record driver confirmation (bridge to world state).
- [app/sensors/sunset.py](app/sensors/sunset.py): Fetches sunrise/sunset times from sunrise-sunset.org for Berlin coordinates and returns whether the sun has set (True/False) or `None` on error.
- [app/sensors/.button.py.swp](app/sensors/.button.py.swp): Editor swap/temporary file; safe to ignore or remove.

## planner/

- [planner/__init__.py](planner/__init__.py): Package marker for planner utilities (empty).
- [planner/problem_generator.py](planner/problem_generator.py): Converts the current `WorldState` into a PDDL `problem.pddl` file by collecting facts (actuator flags, temperature/air quality symbolic facts) and writing a problem text with a goal that typically expresses safe/neutral system state.
- [planner/domain.pddl](planner/domain.pddl): The PDDL domain model describing predicates (e.g., `fan_on`, `temperature_hot`) and actions the planner can use. The planner uses this together with the generated `problem.pddl` to produce a plan.

## zwave-stack/

- [zwave-stack/docker-compose.yml](zwave-stack/docker-compose.yml): Docker Compose stack to run `zwave-js-ui` (Z‑Wave controller UI) and a Mosquitto MQTT broker for local Z-Wave experimentation. Mounts device, volumes and exposes the UI and MQTT ports.
- [zwave-stack/zwave_test.py](zwave-stack/zwave_test.py): A small MQTT consumer/prompter for `zwave/#` messages that extracts sensor names and prints current state; useful when validating Z‑Wave → MQTT payloads.
- [zwave-stack/mosquitto/config/mosquitto.conf](zwave-stack/mosquitto/config/mosquitto.conf): Mosquitto broker configuration (listener, persistence path, log path, allow anonymous).
- Backup/old compose files (.docker-compose_BACKUP.yml, .docker-compose.yml_old, .docker-compose.yml_Backup): historical copies of Docker Compose — safe to keep or clean up.

## debug-test-scripts/

- [debug-test-scripts/relay_toggle.py](debug-test-scripts/relay_toggle.py): Script to toggle all relay outputs periodically via SMBus; handy when testing relay board wiring.
- [debug-test-scripts/relay.py](debug-test-scripts/relay.py): More detailed relay cycling script demonstrating per-relay toggling.
- [debug-test-scripts/ultrasound_buzzer.py](debug-test-scripts/ultrasound_buzzer.py): Standalone test that measures ultrasonic distance and turns a buzzer on when an object is too close.
- [debug-test-scripts/test_mqtt_sensor.py](debug-test-scripts/test_mqtt_sensor.py): Prints `mqtt_state.snapshot()` periodically to monitor incoming MQTT sensor messages.
- [debug-test-scripts/headlights.py](debug-test-scripts/headlights.py): Basic GPIO blink script for the driving lights pin.

## docs/

- [docs/stepByStep.md](docs/stepByStep.md): Deployment and setup notes (Raspberry Pi, Docker, Z‑Wave UI, SSH, quick commands, and tips).
- [docs/System-Flow.md](docs/System-Flow.md): Detailed architecture and flow documentation (sense → plan → act), PDDL explanation, hardware mapping and example scenarios.
- [docs/TODO](docs/TODO): Project TODO list (developer tasks).
- [docs/wichtigeInfos.md](docs/wichtigeInfos.md): Important notes (German) about the project and setup.

## Misc / generated

- `fast-downward/` (ignored in git): Expected location for the Fast Downward planner; `planner_bridge` runs `./fast-downward.py` in this directory. If you want to use Fast Downward, place the planner there or adjust `planner_bridge.py`.
- `planner/problem.pddl` (generated): The problem file produced at runtime by `planner/problem_generator.py` — ignored by `.gitignore`.

---

If you want, I can:
- add cross-references inside each source file as short docstrings, or
- generate a `requirements.txt` inferred from imports and add a quick `scripts/start.sh` runner.

This file was created automatically to document the repository. Last updated: 2026-07-19
