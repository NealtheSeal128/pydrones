"""RC velocity loop demo: continuous velocity + yaw via send_rc_control.

    python control/rc_control.py [--seconds 3]

Flies a gentle forward arc: forward velocity with slight yaw, then stops.
"""

import argparse
import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import hover, mission, rc_hold


def main(seconds=3.0):
    drone = Drone()
    with mission(drone):
        print(f"Forward arc: fb=30, yaw=15 for {seconds}s")
        rc_hold(drone, 0, 30, 0, 15, seconds)
        hover(drone, 1.0)
        print("Strafe: lr=30 for 2s")
        rc_hold(drone, 30, 0, 0, 0, 2.0)
        hover(drone, 1.0)
    print("RC demo complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=3.0)
    args = parser.parse_args()
    main(seconds=args.seconds)
