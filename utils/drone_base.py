"""Shared helpers for pydrones mission scripts.

Built against the verified pysimverse 0.14 API (see requirements.txt):
  Drone(), connect(), take_off(height, speed), land(speed),
  move_forward/backward/left/right/up/down(distance), rotate(angle),
  send_rc_control(lr, fb, ud, yaw), shutdown()
"""

import csv
import time
from contextlib import contextmanager
from datetime import datetime

                                                                           
RC_FRAME = 0.05

RC_MIN = -100
RC_MAX = 100


def safe_rc(lr, fb, ud, yaw):
    """Clamp RC channel values to [-100, 100] ints."""
    return (
        max(RC_MIN, min(RC_MAX, int(lr))),
        max(RC_MIN, min(RC_MAX, int(fb))),
        max(RC_MIN, min(RC_MAX, int(ud))),
        max(RC_MIN, min(RC_MAX, int(yaw))),
    )


def rc_hold(drone, lr, fb, ud, yaw, duration):
    """Send RC values at ~20Hz for ``duration`` seconds, then stop.

    Uses safe_rc() clamping. A final all-zero frame stops motion
    (pysimverse move_* helpers do the same after their timed burst).
    """
    lr, fb, ud, yaw = safe_rc(lr, fb, ud, yaw)
    end = time.time() + duration
    while time.time() < end:
        drone.send_rc_control(lr, fb, ud, yaw)
        time.sleep(RC_FRAME)
    drone.send_rc_control(0, 0, 0, 0)


def hover(drone, duration=1.0):
    """Hold position (all RC axes zero) for ``duration`` seconds."""
    rc_hold(drone, 0, 0, 0, 0, duration)


class DroneLogger:
    """Timestamped in-memory command log with optional CSV export."""

    def __init__(self):
        self.rows = []

    def log(self, action, detail=""):
        self.rows.append((datetime.now().isoformat(timespec="seconds"), action, str(detail)))
        print(f"[log] {action} {detail}".rstrip())

    def save_csv(self, path=None):
        path = path or f"telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "action", "detail"])
            writer.writerows(self.rows)
        print(f"Telemetry saved to {path}")
        return path


@contextmanager
def mission(drone, takeoff_height=100, logger=None):
    """Connect, take off, yield, then land + shutdown even on failure.

    Usage:
        drone = Drone()
        with mission(drone):
            drone.move_forward(50)
    """
    log = logger or DroneLogger()
    drone.connect()
    log.log("connect")
    try:
        drone.take_off(takeoff_height=takeoff_height)
        log.log("take_off", f"height={takeoff_height}")
        yield log
    finally:
        try:
            drone.land()
            log.log("land")
        finally:
            try:
                drone.shutdown()
            except Exception:
                pass
