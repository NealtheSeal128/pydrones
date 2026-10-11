"""Obstacle avoidance: sidestep an obstacle and resume heading.

    python missions/obstacle_avoidance.py [--dist 80]

Simulated obstacle at the midpoint: fly half the leg, sidestep right,
pass, sidestep back left, finish the leg.
"""

import argparse
import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import hover, mission


def main(dist=80):
    drone = Drone()
    with mission(drone) as log:
        half = dist // 2
        drone.move_forward(half)
        log.log("move_forward", half)
        print("Obstacle ahead: sidestepping right.")
        drone.move_right(50)
        log.log("move_right", 50)
        drone.move_forward(half)
        log.log("move_forward", half)
        print("Clear: returning to heading.")
        drone.move_left(50)
        log.log("move_left", 50)
        hover(drone, 1.0)
    print("Obstacle avoidance complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=int, default=80)
    args = parser.parse_args()
    main(dist=args.dist)
