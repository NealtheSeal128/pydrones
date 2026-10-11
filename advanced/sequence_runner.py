"""Execute a JSON mission file.

    python advanced/sequence_runner.py [path]  # default: sample_mission.json

Format: list of {"cmd": ..., ...} steps. Valid cmds:
  move_forward/backward/left/right/up/down (arg), rotate (arg),
  rc (lr/fb/ud/yaw + duration), hover (arg seconds).
"""

import json
import sys

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import hover, mission, rc_hold

VALID = {
    "move_forward", "move_backward", "move_left", "move_right",
    "move_up", "move_down", "rotate", "rc", "hover",
}


def run_step(drone, step, log):
    cmd = step.get("cmd")
    if cmd not in VALID:
        raise ValueError(f"Invalid cmd {cmd!r}. Valid: {sorted(VALID)}")
    if cmd == "rc":
        rc_hold(
            drone,
            step.get("lr", 0), step.get("fb", 0),
            step.get("ud", 0), step.get("yaw", 0),
            step.get("duration", 1.0),
        )
        log.log("rc", step)
    elif cmd == "hover":
        hover(drone, step.get("arg", 1.0))
        log.log("hover", step.get("arg", 1.0))
    elif cmd == "rotate":
        drone.rotate(step["arg"])
        log.log("rotate", step["arg"])
    else:
        getattr(drone, cmd)(step["arg"])
        log.log(cmd, step["arg"])


def main(path="sample_mission.json"):
    with open(path) as f:
        steps = json.load(f)
    print(f"Loaded {len(steps)} steps from {path}")
    drone = Drone()
    with mission(drone) as log:
        for i, step in enumerate(steps):
            print(f"Step {i + 1}/{len(steps)}: {step}")
            run_step(drone, step, log)
    print("Sequence complete.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sample_mission.json")
