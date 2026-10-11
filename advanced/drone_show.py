"""Choreographed multi-drone show with barrier sync.

    python advanced/drone_show.py [--drones 3]

Each drone runs the same beat sequence; a threading.Barrier keeps them
in sync step-by-step, like a light show. Ends with all drones hovering,
then landing together.
"""

import argparse
import sys
import threading

sys.path.insert(0, ".")

from pysimverse import DroneManager

from utils.drone_base import hover

# (description, action) beats. Actions receive (drone, index).
BEATS = [
    ("ascend", lambda d, i: d.move_up(40)),
    ("spread", lambda d, i: d.move_right(40) if i % 2 == 0 else d.move_left(40)),
    ("spin", lambda d, i: d.rotate(180)),
    ("regroup", lambda d, i: d.move_left(40) if i % 2 == 0 else d.move_right(40)),
    ("dip", lambda d, i: d.move_down(20)),
]


def dancer(drone, index, barrier, log_lock):
    for name, action in BEATS:
        action(drone, index)
        with log_lock:
            print(f"drone {index}: {name}")
        barrier.wait()  # sync all drones before next beat
    hover(drone, 1.0)
    barrier.wait()


def main(drone_count=3):
    manager = DroneManager(drone_count=drone_count)
    manager.create_drones()
    rows = [manager.drone_list]
    manager.takeoff_all_drones(rows)

    barrier = threading.Barrier(len(manager.drone_list))
    log_lock = threading.Lock()
    threads = [
        threading.Thread(target=dancer, args=(drone, i, barrier, log_lock))
        for i, drone in enumerate(manager.drone_list)
    ]
    try:
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print("Drone show complete.")
    finally:
        for drone in manager.drone_list:
            try:
                drone.land()
            except Exception:
                pass
            try:
                drone.shutdown()
            except Exception:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--drones", type=int, default=3)
    args = parser.parse_args()
    main(drone_count=args.drones)
