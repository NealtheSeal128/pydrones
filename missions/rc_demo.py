"""RC demo mission: simultaneous velocity + yaw.

    python missions/rc_demo.py
"""

import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import hover, mission, rc_hold


def main():
    drone = Drone()
    with mission(drone) as log:
        rc_hold(drone, 0, 40, 0, 20, 2.0)
        log.log("rc", "fb=40 yaw=20 2s")
        hover(drone, 1.0)
        rc_hold(drone, -30, 0, 10, 0, 2.0)
        log.log("rc", "lr=-30 ud=10 2s")
        hover(drone, 1.0)
    print("RC demo complete.")


if __name__ == "__main__":
    main()
