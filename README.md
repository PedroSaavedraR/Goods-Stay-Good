# Goods-Stay-Good

A research and prototype project for Smart Cities and IoT experimentation. "Goods-Stay-Good" integrates sensor hardware, MQTT messaging, Z-Wave devices, and a symbolic planner to demonstrate automated monitoring and response scenarios (e.g., intrusion detection, environmental monitoring, and actuator control). The repository contains the runtime app, hardware drivers, sensor readers, planner integration, world state management, and debugging scripts.

This README is intended as a comprehensive guide for users, developers, and contributors: how the system is organized, how to set it up on typical hardware (Raspberry Pi), how to run and test components, and where to extend or integrate additional devices and planners.

Table of contents
- Project overview
- Repository layout
- Key components & architecture
- Hardware and prerequisites
- Software prerequisites
- Installation and configuration
- Running the system
- Developer & testing notes
- Troubleshooting & FAQ
- Contributing
- License & contact

**Project overview**

Goods-Stay-Good is a modular prototype that demonstrates how heterogeneous IoT inputs (ultrasonic sensors, buttons, Z-Wave devices, MQTT sensors) can be collected, represented as a world state, and used by an automated planner to decide actions. Example scenarios include toggling relays, sounding a buzzer, or logging events when certain sensor thresholds are reached.

Goals:
- Provide a compact, modular codebase for research and teaching on IoT + automated planning.
- Offer working examples for Raspberry Pi-based deployments and local testing.
- Show an integration path between low-level hardware drivers and higher-level planning modules.

Repository layout

- `app/` — Main application code and runtime entry points.
	- `main.py` — Primary launcher and high-level orchestration.
	- `executor.py` — Executes planner actions or low-level commands.
	- `planner_bridge.py` — Glue code between the planner and the runtime world state.
	- `hardware/` — Hardware drivers and device abstractions.
		- `buzzer.py` — Buzzer control.
		- `relay.py` — Relay control.
		- `hardware_manager.py` — Abstraction layer for device lifecycle and mapping.
	- `sensors/` — Sensor readers and MQTT integration.
		- `ultrasonic.py` — Ultrasonic distance sensor reader.
		- `button.py` — Button input handling.
		- `mqtt.py` — MQTT client utilities and sensor bridging.
		- `sensor_reader.py` — Centralized polling and sensor data normalization.
		- `sunset.py` — (Utility) sunset time helpers if used in scenarios.
- `planner/` — Planner-related files, PDDL domain, and problem generator.
	- `domain.pddl` — PDDL domain model used by the planner.
	- `problem_generator.py` — Generates planner problems from world state snapshots.
- `world_state/` — Persistent world state and configuration.
	- `world_state.py` — Model and operations for the shared state used by the planner and runtime.
	- `config.json` — Default configuration (device ids, thresholds, MQTT topics).
- `zwave-stack/` — Z-Wave integration experiments and local docker-compose for mosquitto (MQTT).
- `debug-test-scripts/` — Small test scripts for manual hardware interaction and debugging.
- `docs/` — Notes, diagrams, and developer documentation.

Key components & architecture

- Sensors & hardware drivers: Poll or subscribe to hardware/sensor inputs and normalize them into events or world-state updates.
- World state: A central representation (`world_state/world_state.py`) that stores the latest sensor values, device statuses, and metadata used by the planner.
- Planner integration: The `planner` folder contains PDDL domain files; `planner_bridge.py` converts the current world state into a PDDL problem and triggers planning runs.
- Executor: Interprets plan steps and executes physical actions using devices via `hardware/hardware_manager.py` and specific device drivers.
- Messaging: MQTT is used to publish/subscribe sensor updates and coordinate between distributed components when applicable.

Hardware and prerequisites

Recommended hardware for prototype deployments:
- Raspberry Pi 3/4 (or similar Linux single-board computer)
- USB Z-Wave controller (e.g., Aeotec Z-Stick Gen5) — for Z-Wave experiments in `zwave-stack`.
- Ultrasonic sensor (HC-SR04 or compatible)
- Relay module for actuator control
- Piezo buzzer

Software prerequisites

- Python 3.8+ (3.10 recommended)
- pip for installing dependencies
- `mosquitto` (if you plan to run the provided local MQTT broker in `zwave-stack/mosquitto`)
- A planner executable (optional): if using automated planning, install a planner that accepts PDDL (e.g., Fast Downward or other planners). Planner configuration is left to the developer and can be invoked from `planner` code.

Installation and configuration

1) Clone the repository

```bash
git clone https://github.com/PedroSaavedraR/Goods-Stay-Good.git
cd Goods-Stay-Good
```

2) Create a Python virtual environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # macOS / Linux
pip install --upgrade pip
pip install -r requirements.txt  # if provided; otherwise install packages below
```

Common Python packages used by the project (install if `requirements.txt` is absent):

```bash
pip install paho-mqtt jsonschema
```

3) Configure `world_state/config.json`

Edit `world_state/config.json` to set MQTT broker details, device mappings (GPIO pins, relay ids), sensor thresholds, and any planner-specific settings.

4) (Optional) Start a local MQTT broker for testing

You can use the docker-compose file in `zwave-stack` to run a Mosquitto broker locally. The compose file is configured under `zwave-stack/mosquitto/config/mosquitto.conf`.

```bash
cd zwave-stack
docker-compose up -d
```

Running the system

1) Simple local run (no planner):

```bash
python app/main.py
```

This launches the main runtime which initializes sensors, hardware, MQTT client, and the world state loop. Check logs for connected devices and health messages.

2) Running planner flows (example):

- Ensure your planner binary is available and accessible from the `planner` scripts or alter the bridge to call your planner.
- The `planner/problem_generator.py` creates a PDDL problem from the `world_state`. Use the planner to solve and output a plan, then feed it to `app/executor.py` for execution.

Usage examples

- Toggle a relay manually using debug scripts in `debug-test-scripts/` (e.g., `relay_toggle.py`).
- Run `debug-test-scripts/ultrasound_buzzer.py` to test ultrasonic sensor-triggered buzzer behavior.
- `debug-test-scripts/test_mqtt_sensor.py` shows how to publish sample MQTT sensor messages against the broker for testing.

Developer & testing notes

- Code style: Follow the existing project structure and keep drivers in `app/hardware` and sensor logic in `app/sensors`.
- Adding a new sensor:
	1. Implement a reader in `app/sensors/` (class that normalizes values and emits world state updates).
	2. Add wiring / configuration to `world_state/config.json` (topic names, thresholds).
	3. Add unit or integration tests in a new `tests/` folder.
- Running unit tests: This project does not include a test harness by default; consider adding `pytest` and test files under `tests/`.

Troubleshooting & FAQ

- Q: Sensors are not appearing in the world state.
	- A: Verify that `sensor_reader.py` is running and that MQTT topics match the `config.json` settings. Check the MQTT broker is reachable.
- Q: Planner returns no plan.
	- A: Verify the generated PDDL problem is valid (print the problem file from `problem_generator.py`) and that the domain file `planner/domain.pddl` matches the predicates used. Try running your planner manually on the domain/problem pair to inspect errors.
- Q: Z-Wave devices not discovered.
	- A: Ensure the Z-Wave controller is attached and recognized by the OS, and that any Z-Wave service/stack is configured. Z-Wave code in `zwave-stack` is experimental and may require driver/config adjustments for your stick.


License & contact

This repository includes a `LICENSE` file at the project root. Refer to it for license details.

For questions or reporting issues, open an issue in the GitHub repository or contact the maintainer listed in `README` metadata or repository settings.

Further reading
- See `docs/` for design notes and step-by-step setup instructions.
- Inspect the example debug scripts in `debug-test-scripts/` to learn concrete run commands.

---
Last updated: 2026

