"""Waypoint navigation: fly through offset waypoints.

    python missions/waypoint_nav.py

Each waypoint is a (forward, right, up) offset from the previous point.
"""

import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import hover, mission

WAYPOINTS = [
    (60, 0, 20),
    (40, 40, 0),
    (0, 40, -10),
    (-30, 0, 10),
]


def fly_offset(drone, fwd, right, up, log):
    if fwd > 0:
        drone.move_forward(fwd)
        log.log("move_forward", fwd)
    elif fwd < 0:
        drone.move_backward(-fwd)
        log.log("move_backward", -fwd)
    if right > 0:
        drone.move_right(right)
        log.log("move_right", right)
    elif right < 0:
        drone.move_left(-right)
        log.log("move_left", -right)
    if up > 0:
        drone.move_up(up)
        log.log("move_up", up)
    elif up < 0:
        drone.move_down(-up)
        log.log("move_down", -up)


def main():
    drone = Drone()
    with mission(drone) as log:
        for i, (fwd, right, up) in enumerate(WAYPOINTS):
            print(f"Waypoint {i + 1}/{len(WAYPOINTS)}: fwd={fwd} right={right} up={up}")
            fly_offset(drone, fwd, right, up, log)
            hover(drone, 0.5)
    print("Waypoint nav complete.")


if __name__ == "__main__":
    main()
