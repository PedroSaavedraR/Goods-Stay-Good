# AI-PLAN — Goods-Stay-Good Refactoring

## Project Overview

Smart truck monitoring system for cargo transport.  
Goal: maintain safe cargo conditions using PDDL-based AI planning.

### Sensors (input)
| Sensor | Source | Data |
|---|---|---|
| Temperature | AEOTEC Z-Wave → MQTT | float °C |
| Humidity | AEOTEC Z-Wave → MQTT | float % |
| Motion (cargo stable?) | AEOTEC Z-Wave → MQTT | bool + timestamp |
| Rear distance | HC-SR04 GPIO | float cm |
| Cargo-check button | GPIO button (pin 17) | press event |
| Outdoor brightness | Internet API (Germany) | bool (sun_has_set) |

### Actuators (output)
| Actuator | Control | Type |
|---|---|---|
| Fan | I²C Relay 3 | on/off |
| Heater | I²C Relay 4 | on/off |
| Status LED (cargo) | I²C Relay 1 | on/off |
| Buzzer (rear alert) | I²C Relay 2 | on/off |
| Driving lights | GPIO 18 | on/off |

### PDDL Domain (smart-truck)
- **Predicates:** temperature_ok/cold/hot, humidity_ok/high/low, cargo_checked/unchecked, rear_clear, driving_lights_on, bright_enough, fan_on, heater_on
- **Goal:** `(and rear_clear cargo_checked temperature_ok humidity_ok)`
- **Missing:** `drive_safe` → `(OutdoorBrightness OR DrivingLightsOn) AND RearClear`

---

## Current Problems

### Critical
1. **`world_state_old.py` uses `changed` boolean** — should use version counter
2. **`sensor_reader.py` returns `Observation` (old) instead of `SensorSnapshot` (model)**
3. **`executor.py` has inline `from hardware import lights`** inside method
4. **`planner/main.py` syntax error** — extra `)` in `mqtt_state.update(...))`
5. **No `sun_has_set` sensor** — Internet brightness API not implemented
6. **No `drive_safe` computation** — formula not implemented anywhere
7. **No automatic buzzer for rear distance** — driver must drive; buzzer not triggered automatically
8. **No automatic status LED for cargo** — LED never turns on/off based on cargo state

### Moderate
9. **No `drive_safe` predicate in PDDL domain**
10. **`humidity_fan_on` action never turns off** — missing `humidity_fan_off` action
11. **Buzzer duplication** — GPIO 4 PWM buzzer (buzzer.py) + I²C Relay 2 buzzer (relay.py)
12. **`SensorSnapshot` unused** — defined in model.py but never instantiated
13. **`Observation` (old) and `SensorSnapshot` (model) coexist** — confusing
14. **Thresholds hardcoded** in world_state_old.py (15, 28, 40, 60, 10) instead of using CONFIG

### Minor
15. **File name `world_state_old.py`** — should be `world_state.py`
16. **No `sensors/sunset.py`** — referenced but missing
17. **`sensors/__init__.py` and `hardware/__init__.py`** are empty — should export modules

---

## Target Architecture

```
Goods-Stay-Good/
├── app/
│   ├── __init__.py
│   ├── main.py              ← orchestrator loop
│   ├── config.py            ← thresholds, GPIO pins, API URL (keep)
│   ├── logger.py            ← logging (keep)
│   ├── model.py             ← SensorSnapshot, Plan (keep, extend)
│   ├── world_state.py       ← rename from world_state_old.py, refactor
│   ├── planner_bridge.py    ← glue: predicates → PDDL → FD → plan
│   ├── executor.py          ← actions → modify world state
│   ├── sensor_reader.py     ← read all sensors → SensorSnapshot
│   ├── sensors/
│   │   ├── __init__.py      ← export read functions
│   │   ├── mqtt.py          ← MQTT listener (keep)
│   │   ├── ultrasonic.py    ← HC-SR04 (keep)
│   │   ├── button.py        ← GPIO button (keep)
│   │   └── sunset.py        ← NEW: Internet API for brightness
│   └── hardware/
│       ├── __init__.py      ← export apply(world) function
│       ├── relay.py         ← I²C relay board (keep)
│       ├── buzzer.py        ← PWM buzzer (keep or merge)
│       └── lights.py        ← GPIO 18 (keep)
├── planner/
│   ├── domain.pddl          ← PDDL model (extend)
│   ├── main.py              ← problem generator (keep)
│   ├── runner.py            ← Fast Downward call (keep)
│   └── parser.py            ← plan output parser (keep)
└── logs/
    └── events.log
```

### Data Flow
```
Sensors → SensorSnapshot → WorldState.apply() → predicates()
    → Planner Bridge → Fast Downward → Plan
    → Executor.step() → WorldState changes
    → Hardware.apply(world)
```

### WorldState Key Design
- **Owns:** temperature, humidity, rear_distance, last_motion, last_cargo_check, sun_has_set, fan_on, heater_on, driving_lights_on
- **Computes:** temperature_state, humidity_state, cargo_checked, rear_clear, drive_safe
- **Exports:** `predicates() → set[str]` for PDDL
- **Versioning:** `world.version += 1` on every state change; planner remembers last_planned_version
- **Replan trigger:** `world.version != last_planned_version AND not goal_reached()`

---

## Refactoring Order (1–10)

### Step 1: Fix critical bugs
- Fix syntax error in `planner/main.py` (extra `)`)
- Fix `executor.py` inline imports (move to top)

### Step 2: Rename & refactor WorldState
- `world_state_old.py` → `world_state.py`
- Convert `changed` boolean → `version: int` counter
- Use `CONFIG` thresholds instead of hardcoded values
- Add `drive_safe` computed property: `(sun_has_set or driving_lights_on) and rear_clear`
- Add `needs_replan(planned_version)` method

### Step 3: Fix sensor_reader + model
- `sensor_reader.py` returns `SensorSnapshot` (from model.py) instead of `Observation`
- Remove `Observation` from world_state_old.py (or keep for backward compat during transition)
- Map MQTT data correctly: temperature, humidity, motion (no illuminance, no UV)

### Step 4: Create sunset sensor
- New file `app/sensors/sunset.py`
- API call to get sunrise/sunset times for Germany
- Returns `sun_has_set: bool`
- Example: `https://api.sunrise-sunset.org/json?lat=51.0&lng=10.0&formatted=0`

### Step 5: Extend PDDL domain
- Add `drive_safe` predicate
- Add `drive_safe` action: `(and (or bright_enough driving_lights_on) rear_clear) → drive_safe`
- Add `humidity_fan_off` action
- Consider removing `bright_enough` (sensor doesn't exist) or replacing with `sun_has_set`

### Step 6: Add automatic buzzer + LED logic
- **Buzzer:** When `rear_clear == False` (and not already buzzing), trigger buzzer. When `rear_clear == True`, stop buzzer.
- **Status LED:** When `cargo == UNCHECKED`, turn LED on. When `cargo == CHECKED`, turn LED off.
- Decide: use GPIO PWM buzzer (buzzer.py) or I²C Relay 2 buzzer (relay.py). Likely keep relay buzzer for simplicity.

### Step 7: Refactor executor
- Remove direct hardware calls from executor
- Executor only modifies WorldState (e.g., `world.fan_on = True`)
- Hardware layer reads WorldState and applies outputs

### Step 8: Refactor hardware layer
- Add `hardware/__init__.py` with `apply(world)` function
- `apply(world)` reads world state and sets GPIO/relays accordingly
- This decouples executor from GPIO

### Step 9: Clean up main loop
- Use version-based replanning
- Add proper error handling
- Add logging of state transitions

### Step 10: Final cleanup
- Remove unused `Observation` dataclass
- Remove commented-out code
- Add `__init__.py` exports
- Test end-to-end

---

## Progress

- [x] Step 1: Fix critical bugs
- [ ] Step 2: Rename & refactor WorldState
- [ ] Step 3: Fix sensor_reader + model
- [ ] Step 4: Create sunset sensor
- [ ] Step 5: Extend PDDL domain
- [ ] Step 6: Add automatic buzzer + LED logic
- [ ] Step 7: Refactor executor
- [ ] Step 8: Refactor hardware layer
- [ ] Step 9: Clean up main loop
- [ ] Step 10: Final cleanup