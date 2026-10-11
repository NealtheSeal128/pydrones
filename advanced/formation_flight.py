"""Multi-drone formation flight via threads.

    python advanced/formation_flight.py [--drones 3 --shape line]

Uses DroneManager (simulator handshake) when the simulator is running.
Each drone gets its own command port from the simulator; takeoff and
formation legs run concurrently in threads.
Shapes: line | v | diamond (diamond needs >= 4 drones).
"""

import argparse
import sys
import threading

sys.path.insert(0, ".")

from pysimverse import DroneManager

SHAPES = ("line", "v", "diamond")


def formation_offsets(shape, count):
    """Lateral/forward offsets per drone index for a shape."""
    if shape == "line":
        return [(0, i * 60) for i in range(count)]
    if shape == "v":
        return [(abs(i - count // 2) * -40, (i - count // 2) * 60) for i in range(count)]
             
    base = [(0, 0), (60, 60), (60, -60), (120, 0)]
    while len(base) < count:
        base.append((len(base) * 40, 0))
    return base[:count]


def fly_offset(drone, fwd, right):
    if fwd > 0:
        drone.move_forward(fwd)
    elif fwd < 0:
        drone.move_backward(-fwd)
    if right > 0:
        drone.move_right(right)
    elif right < 0:
        drone.move_left(-right)


def main(drone_count=3, shape="line"):
    if shape not in SHAPES:
        print(f"Unknown shape {shape}. Choose from {SHAPES}")
        raise SystemExit(1)
    if shape == "diamond" and drone_count < 4:
        print("Diamond needs >= 4 drones; using 4.")
        drone_count = 4

    manager = DroneManager(drone_count=drone_count)
    manager.create_drones()
    print(f"Created {len(manager.drone_list)} drones.")

                                                                                     
    rows = [manager.drone_list[i : i + 2] for i in range(0, len(manager.drone_list), 2)]
    manager.takeoff_all_drones(rows)

    offsets = formation_offsets(shape, len(manager.drone_list))
    threads = []
    try:
        for drone, (fwd, right) in zip(manager.drone_list, offsets):
            t = threading.Thread(target=fly_offset, args=(drone, 80 + fwd, right))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        print(f"Formation '{shape}' complete.")
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
    parser.add_argument("--shape", default="line", choices=SHAPES)
    args = parser.parse_args()
    main(drone_count=args.drones, shape=args.shape)
