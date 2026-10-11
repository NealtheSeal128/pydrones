"""PID altitude-hold controller demo.

    python advanced/pid_hover.py [--target 50 --kp 0.6 --ki 0.05 --kd 0.2]

Since pysimverse move_up/move_down take distances (not velocities), the PID
output is mapped to small corrective climbs/descents each cycle. Gains are
conservative defaults; tune for your simulator scene.
"""

import argparse
import sys
import time

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import mission


class PID:
    def __init__(self, kp, ki, kd, out_limit=30):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.out_limit = out_limit
        self.integral = 0.0
        self.prev_error = 0.0

    def step(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0
        self.prev_error = error
        out = self.kp * error + self.ki * self.integral + self.kd * derivative
        return max(-self.out_limit, min(self.out_limit, out))


def main(target=50, kp=0.6, ki=0.05, kd=0.2, cycles=20):
    drone = Drone()
    with mission(drone) as log:
                                                                         
        altitude = 100.0
        pid = PID(kp, ki, kd)
        dt = 0.5
        for i in range(cycles):
            error = target - (altitude - 100.0)
            correction = pid.step(error, dt)
            step_dist = int(abs(correction))
            if step_dist >= 2:
                if correction > 0:
                    drone.move_up(step_dist)
                else:
                    drone.move_down(step_dist)
                altitude += correction
            log.log("pid", f"cycle={i} err={error:.1f} corr={correction:.1f} alt={altitude - 100.0:.1f}")
            time.sleep(dt)
    print("PID hover complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=float, default=50)
    parser.add_argument("--kp", type=float, default=0.6)
    parser.add_argument("--ki", type=float, default=0.05)
    parser.add_argument("--kd", type=float, default=0.2)
    args = parser.parse_args()
    main(target=args.target, kp=args.kp, ki=args.ki, kd=args.kd)
