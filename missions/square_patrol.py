"""Square patrol: fly a square and return to start.

    python missions/square_patrol.py [--side 60]
"""

import argparse
import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import hover, mission


def main(side=60):
    drone = Drone()
    with mission(drone) as log:
        for i in range(4):
            drone.move_forward(side)
            log.log("move_forward", side)
            drone.rotate(90)
            log.log("rotate", 90)
        hover(drone, 1.0)
    print("Square patrol complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--side", type=int, default=60)
    args = parser.parse_args()
    main(side=args.side)
