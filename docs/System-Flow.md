# Goods-Stay-Good — System Flow & Architecture

## 30-Second Overview

The truck's Raspberry Pi runs a closed **sense → plan → act** loop every 0.5 seconds:

1. **Three sensor sources** (Z-Wave MQTT, GPIO ultrasonic, Internet API) feed raw data into a `SensorSnapshot`
2. The snapshot is **applied** to `WorldState`, which computes symbolic states and emits `predicates()` as PDDL facts
3. If the world changed and the goal isn't reached, a **PDDL planner** (Fast Downward) is called to produce a plan
4. The **executor** pops one action from the plan and toggles the corresponding WorldState boolean
5. The **hardware layer** mirrors WorldState to physical relays and GPIO outputs

---

## Step-by-Step Flow

### PHASE 0 — Background Threads (start on import)

Three things happen as soon as `main.py` starts, before the loop even runs:

**0a. MQTT listener** (`sensors/mqtt.py` → runs on import)
- Creates a `paho-mqtt` client, connects to `localhost:1883` (Mosquitto broker)
- Subscribes to `zwave/#`
- Calls `client.loop_start()` — runs a background thread forever
- Every incoming Z-Wave message triggers `on_message()` → `mqtt_state.update()`
- `update()` parses JSON, extracts `value` and `time`, stores under a `threading.Lock()`:
  - `Air_temperature` → `self.temperature` (float °C)
  - `/Humidity` → `self.humidity` (float %)
  - `Motion_sensor_status` → `self.motion` (bool) + `self.motion_timestamp` (epoch seconds)

**0b. Sunset API** (`sensors/sunset.py` → `SunsetChecker.__init__()` on import)
- Calls `api.sunrise-sunset.org?lat=51.0&lng=10.0&formatted=0`
- Parses ISO 8601 `sunrise` and `sunset` timestamps, stores as UTC epoch floats
- Caches per day — only re-fetches when the date changes

**0c. Cargo button** (`sensors/button.py` → runs on import)
- Attaches `gpiozero.Button` on pin 17
- Registers `when_pressed` callback → `world.acknowledge_cargo()`
- This is the ONLY way `cargo_checked` becomes true — the driver MUST physically press the button

---

### PHASE 1 — Read sensors → SensorSnapshot (every 0.5s)

`main.py` calls `sensor_reader.read()`:

```
read()
  │
  ├─ mqtt_state.snapshot()        ← thread-safe copy of {temp, humidity, motion, motion_timestamp}
  ├─ ultrasonic.get_distance()    ← sends 10µs trigger pulse, measures echo, returns cm (or None on timeout)
  └─ sunset_checker.sun_has_set() ← compares current time to cached sunrise/sunset (or None if API failed)
         │
         ▼
    SensorSnapshot(
        temperature=22.4,
        humidity=55.0,
        motion_detected=False,
        motion_timestamp=None,
        rear_distance=45.2,
        sun_has_set=False
    )
```

### PHASE 2 — WorldState.apply(snapshot) (computes symbolic state)

```
world.apply(snapshot)
  │
  ├─ Copies raw float values: self.temperature, self.humidity, self.rear_distance, self.sun_has_set
  ├─ If motion detected AND timestamp > cargo_last_checked → self.last_motion = timestamp
  │     (marks cargo as potentially disturbed — needs re-check)
  │
  └─ Calls self.predicates() before/after to detect change → if different, self.version += 1
```

**Computed properties** (derived from raw values, no storage needed):

| Property | Logic | Example |
|---|---|---|
| `temperature_state` | `< 15 → COLD, > 28 → HOT, else OK` | `TemperatureState.OK` |
| `humidity_state` | `< 40 → LOW, > 60 → HIGH, else OK` | `HumidityState.OK` |
| `rear_clear` | `distance > 10cm or None → True` | `True` |
| `cargo_checked` | `last_motion ≤ cargo_last_checked` | `True` |
| `drive_safe` | `(not sun_has_set OR driving_lights_on) AND rear_clear` | `True` |

### PHASE 3 — predicates() → PDDL facts

`world.predicates()` is called to produce a set of strings:

```
{temperature_ok, humidity_ok, cargo_checked, rear_clear, drive_safe, sun_has_set}
```

### PHASE 4 — Planner (only when needed)

`main.py` checks: `world.needs_replan(last_planned_version) OR not executor.plan`
- If the world version hasn't changed since last plan AND a plan still exists → skip
- If goal already reached → skip
- Otherwise: call `planner_bridge.create_plan(world)`

```
create_plan(world)
  │
  ├─ planner/main.py:create_problem(world)
  │     │
  │     ├─ facts = [f"({p})" for p in world.predicates()]
  │     ├─ Goal: (and (drive_safe) (cargo_checked) (temperature_ok) (humidity_ok))
  │     └─ Writes PDDL problem file to planner/problem.pddl
  │
  ├─ subprocess.run(["python3", "fast-downward/fast-downward.py",
  │                   "planner/domain.pddl", "planner/problem.pddl",
  │                   "--search", "astar(lmcut)"])
  │
  └─ Parses Fast Downward output:
        "Plan:" section → extracts action names → returns list of strings
```

Example plan for a scenario where temperature is hot and cargo unchecked:
```
["fan_on", "status_led_on"]
```
(Planner found: turn on fan for cooling, turn on LED to remind driver to check cargo)

### PHASE 5 — Execute one action

`executor.execute_next(world)` pops the first action:

```
action = "fan_on"

if action == "fan_on":
    world.fan_on = True          ← only touches WorldState, no hardware
elif action == "fan_off":
    world.fan_on = False
elif action == "heater_on":
    world.heater_on = True
# ... 9 more action types ...
elif action == "status_led_off":
    world.status_led_on = False

world.version += 1               ← always increments after an action
```

This is **pure logic** — no imports from `hardware`. The executor only flips booleans on the WorldState object.

### PHASE 6 — Mirror to hardware

`hardware.apply(world)` compares each field to its previous value:

```
if world.fan_on != _prev_fan_on:
    if world.fan_on:
        relay.fan_on()           ← I²C set_relay(3, True)
    else:
        relay.fan_off()          ← I²C set_relay(3, False)
    _prev_fan_on = world.fan_on

# Same pattern for: heater (relay 4), buzzer (relay 2),
#                    status LED (relay 1), driving lights (GPIO 18)
```

Only changes trigger physical writes — if nothing changed, no hardware is touched.

---

## The PDDL Domain — What the Planner Knows

### 15 Predicates (symbolic facts)

```
temperature_ok   temperature_hot   temperature_cold
humidity_ok      humidity_high     humidity_low
cargo_checked    cargo_unchecked
rear_clear
driving_lights_on   sun_has_set
fan_on   heater_on   buzzer_on   status_led_on
```

### 11 Actions (what the planner can do)

| # | Action | When available | What happens |
|---|---|---|---|
| 1 | `fan_on` | temp hot OR humidity extreme | Fan turns on |
| 2 | `fan_off` | temp OK AND humidity OK | Fan turns off |
| 3 | `heater_on` | temp cold | Heater turns on |
| 4 | `heater_off` | temp OK | Heater turns off |
| 5 | `check_cargo` | cargo unchecked | Driver pressed button (cargo checked) |
| 6 | `turn_lights_on` | sun has set | Driving lights on |
| 7 | `turn_lights_off` | sun not set | Driving lights off |
| 8 | `buzzer_on` | rear not clear | Buzzer alert |
| 9 | `buzzer_off` | rear clear | Buzzer stops |
| 10 | `status_led_on` | cargo unchecked | LED reminds driver |
| 11 | `status_led_off` | cargo checked | LED off |

### Goal
```lisp
(and (drive_safe) (cargo_checked) (temperature_ok) (humidity_ok))
```

Key design note: `drive_safe` is NOT a PDDL action — it's a **computed property** in WorldState. The planner sees it as a fact that becomes true when `(not sun_has_set OR driving_lights_on) AND rear_clear`. The planner can make `drive_safe` true by turning on lights (if dark) or by waiting for the driver to clear the rear.

---

## Concrete Example Walkthrough

**Scenario:** Truck is parked, it's nighttime, cargo area is too hot (30°C), and motion was just detected.

```
Tick 1:
  read() → SensorSnapshot(temp=30.0, humidity=50, motion_detected=True,
                          motion_timestamp=1700000000, rear_distance=45, sun_has_set=True)
  world.apply(snapshot) → temperature_state=HOT, cargo_checked=False, version=1
  predicates() → {temperature_hot, humidity_ok, cargo_unchecked, rear_clear, sun_has_set}
  world.needs_replan(-1) → True
  create_plan(world) → Fast Downward returns: ["fan_on", "status_led_on", "turn_lights_on"]
  executor.execute_next() → world.fan_on = True, version=2
  hardware.apply() → relay.fan_on() called

Tick 2:
  read() → (same values, world hasn't changed)
  world.apply() → no change, version stays 2
  Plan still has ["status_led_on", "turn_lights_on"]
  executor.execute_next() → world.status_led_on = True, version=3
  hardware.apply() → relay.status_led_on() called

Tick 3:
  executor.execute_next() → world.driving_lights_on = True, version=4
  hardware.apply() → lights.driving_lights_on() called

Tick 4:
  Plan empty. predicates() → {temperature_hot, humidity_ok, cargo_unchecked, rear_clear,
                              sun_has_set, fan_on, status_led_on, driving_lights_on, drive_safe}
  world.goal_reached() → False (cargo_unchecked, temperature_hot)
  world.needs_replan(4) → True (cargo still unchecked, temp still hot — but plan is empty
                                because fan is already on, LED is on, lights are on)
  create_plan() → returns [] (nothing more the planner can do)
  No action executed this tick. System waits for:
    - Temperature to drop below 28°C (fan will cool it down)
    - Driver to press cargo-check button (LED is on as reminder)

Tick 5 (temperature now 27°C, driver pressed button):
  world.apply() → temperature_state=OK, cargo_checked=True, version=5
  predicates() → {temperature_ok, humidity_ok, cargo_checked, rear_clear,
                  sun_has_set, fan_on, status_led_on, driving_lights_on, drive_safe}
  world.goal_reached() → True!
  needs_replan() → False (goal reached, no replan needed)
  Plan stays empty. Hardware stays as-is (fan on, LED on, lights on — but goal reached).
```

---

## Hardware Mapping

| Actuator | Control Method | Pin/Address |
|---|---|---|
| Status LED | I²C Relay 1 (PCAL9535A) | 0x20, bit 0 |
| Buzzer | I²C Relay 2 (PCAL9535A) | 0x20, bit 1 |
| Fan | I²C Relay 3 (PCAL9535A) | 0x20, bit 2 |
| Heater | I²C Relay 4 (PCAL9535A) | 0x20, bit 3 |
| Driving Lights | GPIO output | Pin 18 |
| ~~Buzzer PWM~~ | ~~GPIO PWM 500Hz~~ | ~~Pin 4 (DEPRECATED)~~ |

Relays are **active LOW** — writing `0` to the bit turns the relay ON.

---

## File Map

| File | Role | Lines |
|---|---|---|
| `app/main.py` | Orchestrator loop (read → plan → execute → apply) | 42 |
| `app/config.py` | Thresholds, pins, API coordinates | 47 |
| `app/logger.py` | Logging to file (`log/events.log`) + console | 22 |
| `app/model.py` | `SensorSnapshot`, `Plan` dataclasses | 20 |
| `app/world_state.py` | Raw values → symbolic states → PDDL facts | 120 |
| `app/sensor_reader.py` | Aggregates all sensors → one `SensorSnapshot` | 25 |
| `app/executor.py` | Plan execution → WorldState fields only (no HW) | 56 |
| `app/planner_bridge.py` | Fast Downward subprocess + output parser | 70 |
| `app/sensors/mqtt.py` | MQTT listener (background thread, Z-Wave) | 82 |
| `app/sensors/ultrasonic.py` | HC-SR04 distance measurement (GPIO) | 72 |
| `app/sensors/button.py` | GPIO cargo-check button (pin 17) | 19 |
| `app/sensors/sunset.py` | Internet sunset API + daily cache | 64 |
| `app/hardware/__init__.py` | `apply(world)` — mirrors WorldState → physical | 60 |
| `app/hardware/relay.py` | I²C PCAL9535A 4-relay board driver | 112 |
| `app/hardware/lights.py` | GPIO 18 driving lights | 40 |
| `app/hardware/buzzer.py` | GPIO 4 PWM buzzer (DEPRECATED) | 28 |
| `planner/domain.pddl` | PDDL domain: 15 predicates, 11 actions | 120 |
| `planner/main.py` | Problem generator: predicates → PDDL file | 60 |

