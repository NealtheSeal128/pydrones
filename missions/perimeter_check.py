"""Perimeter check: high-altitude rectangle patrol.

    python missions/perimeter_check.py [--length 120 --width 80]
"""

import argparse
import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import hover, mission


def main(length=120, width=80):
    drone = Drone()
    with mission(drone, takeoff_height=150) as log:
        for side in (length, width, length, width):
            drone.move_forward(side)
            log.log("move_forward", side)
            drone.rotate(90)
            log.log("rotate", 90)
        hover(drone, 1.0)
    print("Perimeter check complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=120)
    parser.add_argument("--width", type=int, default=80)
    args = parser.parse_args()
    main(length=args.length, width=args.width)
