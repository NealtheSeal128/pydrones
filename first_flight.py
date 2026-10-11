"""First flight: basic movements smoke test.

Run the simulator first, then:
    python first_flight.py [--height 100]
"""

import argparse
import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import hover, mission


def main(height=100):
    drone = Drone()
    with mission(drone, takeoff_height=height) as log:
        drone.move_forward(50)
        log.log("move_forward", 50)
        drone.move_backward(50)
        log.log("move_backward", 50)
        drone.move_left(50)
        log.log("move_left", 50)
        drone.move_right(50)
        log.log("move_right", 50)
        drone.move_up(30)
        log.log("move_up", 30)
        drone.move_down(30)
        log.log("move_down", 30)
        drone.rotate(90)
        log.log("rotate", 90)
        hover(drone, 1.0)
        log.log("hover", 1.0)
    print("First flight complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--height", type=int, default=100)
    args = parser.parse_args()
    main(height=args.height)
