"""Figure-8 via RC arc pairs.

    python missions/figure_eight.py [--seconds 2.5]

Two mirrored arcs: forward + right yaw, then forward + left yaw.
"""

import argparse
import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import hover, mission, rc_hold


def main(seconds=2.5):
    drone = Drone()
    with mission(drone) as log:
        print("Arc 1: forward + right yaw")
        rc_hold(drone, 0, 35, 0, 25, seconds)
        log.log("rc", f"fb=35 yaw=25 {seconds}s")
        print("Arc 2: forward + left yaw")
        rc_hold(drone, 0, 35, 0, -25, seconds)
        log.log("rc", f"fb=35 yaw=-25 {seconds}s")
        hover(drone, 1.0)
    print("Figure-8 complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=2.5)
    args = parser.parse_args()
    main(seconds=args.seconds)
