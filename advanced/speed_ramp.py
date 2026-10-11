"""Smooth acceleration/deceleration (speed ramp) demo.

    python advanced/speed_ramp.py [--peak 60 --steps 5]
"""

import argparse
import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import hover, mission, rc_hold


def main(peak=60, steps=5):
    drone = Drone()
    with mission(drone) as log:
        print("Ramping up:")
        for i in range(1, steps + 1):
            vel = int(peak * i / steps)
            rc_hold(drone, 0, vel, 0, 0, 0.5)
            log.log("ramp_up", f"fb={vel}")
        print("Ramping down:")
        for i in range(steps, 0, -1):
            vel = int(peak * i / steps)
            rc_hold(drone, 0, vel, 0, 0, 0.5)
            log.log("ramp_down", f"fb={vel}")
        hover(drone, 1.0)
    print("Speed ramp complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--peak", type=int, default=60)
    parser.add_argument("--steps", type=int, default=5)
    args = parser.parse_args()
    main(peak=args.peak, steps=args.steps)
