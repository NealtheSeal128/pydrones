"""Return-to-home: record outbound moves, reverse them to return.

    python missions/return_to_home.py

Outbound path is recorded as (method, arg) pairs; RTH plays the inverse
in reverse order (forward<->backward, left<->right, up<->down, rotate negated).
"""

import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import hover, mission

INVERSE = {
    "move_forward": "move_backward",
    "move_backward": "move_forward",
    "move_left": "move_right",
    "move_right": "move_left",
    "move_up": "move_down",
    "move_down": "move_up",
}

OUTBOUND = [
    ("move_forward", 60),
    ("move_right", 40),
    ("move_up", 30),
    ("move_forward", 50),
]


def main():
    drone = Drone()
    with mission(drone) as log:
        print("Outbound leg:")
        for method, arg in OUTBOUND:
            getattr(drone, method)(arg)
            log.log(method, arg)
        hover(drone, 1.0)
        print("Returning home:")
        for method, arg in reversed(OUTBOUND):
            if method == "rotate":
                drone.rotate(-arg)
                log.log("rotate", -arg)
            else:
                inv = INVERSE[method]
                getattr(drone, inv)(arg)
                log.log(inv, arg)
        hover(drone, 1.0)
    print("Return-to-home complete.")


if __name__ == "__main__":
    main()
