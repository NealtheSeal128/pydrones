"""Orbit a central point: N tangent segments with yaw steps.

    python missions/orbit.py [--segments 8 --seg-dist 30]
"""

import argparse
import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import hover, mission


def main(segments=8, seg_dist=30):
    drone = Drone()
    with mission(drone) as log:
        yaw_step = 360 // segments
        for i in range(segments):
            drone.move_forward(seg_dist)
            log.log("move_forward", seg_dist)
            drone.rotate(yaw_step)
            log.log("rotate", yaw_step)
        hover(drone, 1.0)
    print("Orbit complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--segments", type=int, default=8)
    parser.add_argument("--seg-dist", type=int, default=30)
    args = parser.parse_args()
    main(segments=args.segments, seg_dist=args.seg_dist)
