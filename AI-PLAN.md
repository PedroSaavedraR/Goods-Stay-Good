# AI-PLAN — Goods-Stay-Good

## Project Purpose

A **smart truck cargo monitoring system** running on a Raspberry Pi 3. It uses **PDDL-based AI planning** (Fast Downward with `astar(lmcut)`) to autonomously maintain safe environmental and safety conditions for transported goods.

The system reads real-world sensor data, translates it into a symbolic world state, feeds it to a PDDL planner, and executes the resulting plan by controlling physical actuators — all in a closed loop.

---

## Hardware Inventory

### Sensors (Input → WorldState)

| Sensor | Protocol | Hardware | What It Provides |
|---|---|---|---|
| Temperature | Z-Wave → MQTT (`zwave/#`) | AEOTEC sensor via Z-Stick Gen5 → zwave-js-ui Docker → Mosquitto | `temperature` (°C float) |
| Humidity | Z-Wave → MQTT | Same AEOTEC sensor | `humidity` (% float) |
| PIR Motion | Z-Wave → MQTT | Same AEOTEC sensor | `motion` (bool) + `motion_timestamp` (epoch) |
| Rear Distance | GPIO | HC-SR04 ultrasonic (TRIG=22, ECHO=27) | `rear_distance` (cm float) |
| Cargo-Check Button | GPIO | Button on pin 17 (`gpiozero`) | Calls `world.acknowledge_cargo()` on press |
| Outdoor Brightness | Internet API | `sunrise-sunset.org` (lat=51.0, lng=10.0, Germany) | `sun_has_set` (bool) — cached once per day |

### Actuators (WorldState → Output)

| Actuator | Hardware | PDDL Action | Behavior |
|---|---|---|---|
| **Status LED** | I²C Relay 1 (PCAL9535A @ 0x20) | `status_led_on` / `status_led_off` | Lights up when cargo is unchecked (motion detected). Stays on until driver presses the cargo-check button. |
| **Buzzer** | I²C Relay 2 | `buzzer_on` / `buzzer_off` | Audible alert when rear is not clear. Driver must move the truck forward until rear clears — then buzzer stops automatically. |
| **Fan** | I²C Relay 3 | `fan_on` / `fan_off` | Serves dual purpose: (1) cooling when too hot, (2) humidity control when too high or low. PDDL balances both — fan only turns off when temperature AND humidity are OK. |
| **Heater (lamp)** | I²C Relay 4 | `heater_on` / `heater_off` | Heats cargo when temperature is too cold. |
| **Driving Lights** | GPIO 18 | `turn_lights_on` / `turn_lights_off` | Turns on when sun has set (dark). Turns off when sun rises again — saves power. |
| ~~Buzzer PWM~~ | GPIO 4 (500Hz) | — | **Deprecated duplicate.** The relay-based buzzer (Relay 2) is the primary one. This file exists but is no longer used. |

---

## Architecture

```
Goods-Stay-Good/
├── app/
│   ├── main.py              ← Orchestrator loop (read → plan → execute → apply)
│   ├── config.py            ← All thresholds, pins, API coordinates
│   ├── logger.py            ← Logging
│   ├── model.py             ← SensorSnapshot, Plan dataclasses
│   ├── world_state.py       ← WorldState: raw values → computed states → PDDL predicates
│   ├── planner_bridge.py    ← Calls Fast Downward, parses plan output
│   ├── executor.py          ← Executes plan actions → modifies WorldState only (no HW)
│   ├── sensor_reader.py     ← Aggregates all sensors → SensorSnapshot
│   ├── sensors/
│   │   ├── mqtt.py          ← MQTT listener (Z-Wave: temp, humidity, motion)
│   │   ├── ultrasonic.py    ← HC-SR04 rear distance sensor
│   │   ├── button.py        ← GPIO cargo-check button
│   │   └── sunset.py        ← Internet API: sunrise-sunset.org
│   └── hardware/
│       ├── __init__.py      ← apply(world): mirrors WorldState → physical GPIO/relays
│       ├── relay.py         ← I²C PCAL9535A 4-relay board
│       ├── buzzer.py        ← PWM buzzer (DEPRECATED — kept for reference)
│       └── lights.py        ← GPIO 18 driving lights
├── planner/
│   ├── domain.pddl          ← PDDL domain: predicates + actions
│   └── main.py              ← Problem generator: world.predicates() → PDDL problem file
└── logs/
    └── events.log
```

### Data Flow

```
 ┌──────────────────────────────────────────────────────────┐
 │                     MAIN LOOP (0.5s)                     │
 │                                                          │
 │  1. sensor_reader.read()                                 │
 │     ├── mqtt_state.snapshot()  (temp, humidity, motion)  │
 │     ├── ultrasonic.get_distance()                        │
 │     └── sunset_checker.sun_has_set()                     │
 │              ↓                                           │
 │  2. world.apply(snapshot)                                │
 │     Raw values → computed states (temperature_ok/hot/cold│
 │     humidity_ok/high/low, rear_clear, cargo_checked,     │
 │     drive_safe) → version++ if changed                   │
 │              ↓                                           │
 │  3. world.needs_replan()? → planner_bridge.create_plan() │
 │     world.predicates() → PDDL problem → Fast Downward    │
 │              ↓                                           │
 │  4. executor.execute_next(world)                         │
 │     One action per tick → modifies world.fan_on, etc.    │
 │              ↓                                           │
 │  5. hardware.apply(world)                                │
 │     WorldState → relay.set_relay() / GPIO.output()       │
 └──────────────────────────────────────────────────────────┘
```

---

## WorldState Design

### Raw Fields (set by `apply(snapshot)`)
| Field | Type | Source |
|---|---|---|
| `temperature` | `float \| None` | MQTT |
| `humidity` | `float \| None` | MQTT |
| `rear_distance` | `float \| None` | Ultrasonic |
| `sun_has_set` | `bool` | sunset.py API |
| `last_motion` | `float \| None` | MQTT (timestamp) |
| `cargo_last_checked` | `float` | Button press timestamp |

### Actuator Fields (set by `executor`)
| Field | Type | Default |
|---|---|---|
| `fan_on` | `bool` | `False` |
| `heater_on` | `bool` | `False` |
| `driving_lights_on` | `bool` | `False` |
| `buzzer_on` | `bool` | `False` |
| `status_led_on` | `bool` | `False` |

### Computed Properties
| Property | Logic |
|---|---|
| `temperature_state` | `< 15°C → COLD, > 28°C → HOT, else OK` |
| `humidity_state` | `< 40% → LOW, > 60% → HIGH, else OK` |
| `rear_clear` | `rear_distance > 10cm` (or `None` → `True`) |
| `cargo_checked` | `last_motion <= cargo_last_checked` |
| `drive_safe` | `(not sun_has_set OR driving_lights_on) AND rear_clear` |

### `predicates() → set[str]`
Emits: `temperature_ok/hot/cold`, `humidity_ok/high/low`, `cargo_checked/unchecked`, `rear_clear`, `drive_safe`, `driving_lights_on`, `sun_has_set`, `fan_on`, `heater_on`, `buzzer_on`, `status_led_on`

### Versioning
- `world.version` increments on every state change (predicates differ) or executor action
- `needs_replan(planned_version)` returns `True` when `world.version != planned_version AND not goal_reached()`

---

## PDDL Domain

### Predicates
`temperature_ok`, `temperature_hot`, `temperature_cold`, `humidity_ok`, `humidity_high`, `humidity_low`, `cargo_checked`, `cargo_unchecked`, `rear_clear`, `driving_lights_on`, `sun_has_set`, `fan_on`, `heater_on`, `buzzer_on`, `status_led_on`

### Actions

| Action | Precondition | Effect |
|---|---|---|
| `fan_on` | `temperature_hot` OR `humidity_high` OR `humidity_low` | `fan_on` |
| `fan_off` | `temperature_ok` AND `humidity_ok` | `not fan_on` |
| `heater_on` | `temperature_cold` | `heater_on` |
| `heater_off` | `temperature_ok` | `not heater_on` |
| `check_cargo` | `cargo_unchecked` | `cargo_checked`, `not cargo_unchecked` |
| `turn_lights_on` | `sun_has_set` | `driving_lights_on` |
| `turn_lights_off` | `not sun_has_set` | `not driving_lights_on` |
| `buzzer_on` | `not rear_clear` | `buzzer_on` |
| `buzzer_off` | `rear_clear` | `not buzzer_on` |
| `status_led_on` | `cargo_unchecked` | `status_led_on` |
| `status_led_off` | `cargo_checked` | `not status_led_on` |

### Goal
```lisp
(and (drive_safe) (cargo_checked) (temperature_ok) (humidity_ok))
```

---

## Key Design Decisions

1. **Everything goes through PDDL.** Even "obvious" behaviors like buzzer-on-rear-unclear and LED-on-cargo-unchecked are PDDL actions. The planner decides when to activate/deactivate them. This keeps the system a pure sense→plan→act loop.

2. **Fan serves dual purpose.** The fan cools AND controls humidity. `fan_off` requires BOTH `temperature_ok` AND `humidity_ok` — the planner must find a balance if both are out of range.

3. **Executor is pure logic.** It only modifies `WorldState` fields. No hardware calls. The `hardware/__init__.py` layer reads `WorldState` and mirrors it to physical outputs with change-detection.

4. **Version-based replanning.** Instead of a `changed` boolean, every state change increments a version counter. The planner only replans when the version differs AND the goal is not yet reached.

5. **Relay buzzer is primary.** The GPIO 4 PWM buzzer (`buzzer.py`) is deprecated. The I²C relay buzzer (Relay 2) is the one used.

---

## Progress

- [x] Step 1: Fix critical bugs (syntax error, inline imports)
- [x] Step 2: Rename & refactor WorldState (version counter, CONFIG thresholds, `drive_safe`, `needs_replan`)
- [x] Step 3: Fix sensor_reader + model (returns `SensorSnapshot`, main calls `world.apply`)
- [x] Step 4: Create sunset sensor (`sunset.py` with daily-cached API)
- [x] Step 5: Extend PDDL domain (buzzer, status LED, `turn_lights_off`, fan combined precondition, `sun_has_set` replaces `bright_enough`)
- [x] Step 6: Add buzzer + LED PDDL actions (buzzer triggered by `not rear_clear`, LED by `cargo_unchecked`)
- [x] Step 7: Refactor executor (no hardware imports, only modifies WorldState, all 10 actions)
- [x] Step 8: Refactor hardware layer (`hardware/__init__.py` with `apply(world)` and change-detection)
- [x] Step 9: Clean up main loop (error handling, logging, `hardware_apply(world)` after each tick)
- [ ] Step 10: Final cleanup (remove legacy `Observation`, `update()`, add `__init__.py` exports)

---

## Remaining Cleanup (Step 10)

1. **`world_state.py`**: Remove the legacy `Observation` dataclass and `update()` method — only `apply(snapshot: SensorSnapshot)` is needed now
2. **`app/__init__.py`**: Add exports
3. **`app/sensors/__init__.py`**: Add exports
4. **`app/hardware/__init__.py`**: Exports already done ✅
5. **`app/config.py`**: Missing `from dataclasses import dataclass` import — needs to be added