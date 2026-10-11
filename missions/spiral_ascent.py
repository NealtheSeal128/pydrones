"""Spiral ascent: rotate while climbing to a target altitude.

    python missions/spiral_ascent.py [--turns 4 --climb 25]
"""

import argparse
import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import mission


def main(turns=4, climb=25):
    drone = Drone()
    with mission(drone) as log:
        for i in range(turns):
            drone.rotate(90)
            log.log("rotate", 90)
            drone.move_up(climb)
            log.log("move_up", climb)
    print("Spiral ascent complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--turns", type=int, default=4)
    parser.add_argument("--climb", type=int, default=25)
    args = parser.parse_args()
    main(turns=args.turns, climb=args.climb)
