"""Zigzag (lawnmower) sweep coverage.

    python missions/zigzag.py [--lanes 4 --lane-len 80 --lane-gap 40]
"""

import argparse
import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import hover, mission


def main(lanes=4, lane_len=80, lane_gap=40):
    drone = Drone()
    with mission(drone) as log:
        for lane in range(lanes):
            drone.move_forward(lane_len)
            log.log("move_forward", lane_len)
            if lane < lanes - 1:
                if lane % 2 == 0:
                    drone.move_right(lane_gap)
                    log.log("move_right", lane_gap)
                    drone.rotate(90)
                    drone.move_forward(lane_gap)
                    drone.rotate(90)
                    log.log("turnaround", "right")
                else:
                    drone.move_left(lane_gap)
                    log.log("move_left", lane_gap)
                    drone.rotate(-90)
                    drone.move_forward(lane_gap)
                    drone.rotate(-90)
                    log.log("turnaround", "left")
        hover(drone, 1.0)
    print("Zigzag sweep complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lanes", type=int, default=4)
    parser.add_argument("--lane-len", type=int, default=80)
    parser.add_argument("--lane-gap", type=int, default=40)
    args = parser.parse_args()
    main(lanes=args.lanes, lane_len=args.lane_len, lane_gap=args.lane_gap)
