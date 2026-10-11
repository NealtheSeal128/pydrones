# pydrones

PySimVerse drone mission pack (`pysimverse==0.14`, Python ≥ 3.9).
Original implementations using only the verified `pysimverse` API —
no invented methods.

## Setup

1. Install the PySimVerse simulator from <https://pysimverse.com/> and start it.
2. Create a venv and install deps:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

3. Smoke test the API (no simulator needed for import check):

```bash
python -c "from pysimverse import Drone; print([m for m in dir(Drone) if not m.startswith('_')])"
```

## Confirmed API (v0.14)

`Drone()`, `connect()`, `take_off(height, speed)`, `land()`,
`move_forward/backward/left/right/up/down(distance)`, `rotate(angle)`,
`send_rc_control(lr, fb, ud, yaw)`, `shutdown()`.
Multi-drone via `DroneManager(drone_count)` + `create_drones()`.

## Layout

```text
first_flight.py            basic movements smoke test
utils/drone_base.py        rc_hold, hover, safe_rc, DroneLogger, mission()
control/keyboard_control.py  WASD + arrows (pynput)
control/gamepad_control.py   gamepad via pygame
control/rc_control.py        RC velocity loop demo
missions/                  10 scripted missions (square, spiral, obstacle, ...)
advanced/                  formation, show, pid_hover, speed_ramp, sequence_runner
sample_mission.json        example for sequence_runner
```

## Run

```bash
python first_flight.py
python control/keyboard_control.py   # T take off, Q quit+land
python control/rc_control.py
python missions/square_patrol.py
python missions/zigzag.py
python missions/return_to_home.py
python advanced/speed_ramp.py
python advanced/sequence_runner.py                 # uses sample_mission.json
python advanced/sequence_runner.py my_mission.json # custom
# multi-drone (needs simulator): python advanced/formation_flight.py --drones 3 --shape v
```

JSON mission steps: `move_forward/backward/left/right/up/down` (`arg`),
`rotate` (`arg`), `rc` (`lr/fb/ud/yaw/duration`), `hover` (`arg` seconds).

## Safety

Every script takes off and lands inside `utils.drone_base.mission()`,
which guarantees `land()` + `shutdown()` even on exceptions.
