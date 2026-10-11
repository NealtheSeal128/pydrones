"""Real-time keyboard control.

    python control/keyboard_control.py

Keys:
  W/S forward/back, A/D left/right,
  Up/Down ascend/descend, Left/Right yaw,
  T take off, L land, Space hover-stop, Q quit+land.

Requires: pip install pynput (macOS: grant Input Monitoring permission).
"""

import sys
import threading

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import RC_FRAME, hover

STEP = 40  # RC magnitude per keypress burst


def print_help():
    print("W/S fwd/back | A/D left/right | Up/Down up/down | Left/Right yaw")
    print("T take off | L land | Space hover | Q quit")


def main():
    try:
        from pynput import keyboard
    except ImportError:
        print("pynput not installed. Run: pip install pynput")
        raise SystemExit(1)

    drone = Drone()
    drone.connect()
    print_help()
    print("Press T to take off. Q quits (lands first).")

    state = {"flying": False, "quit": False}

    def on_press(key):
        try:
            k = key.char.lower() if key.char else None
        except AttributeError:
            k = None
        name = getattr(key, "name", None)

        if k == "q" or name == "q":
            state["quit"] = True
            return False  # stop listener
        if k == "t":
            if not state["flying"]:
                drone.take_off()
                state["flying"] = True
            return
        if k == "l":
            if state["flying"]:
                drone.land()
                state["flying"] = False
            return
        if not state["flying"]:
            return
        if k == "w":
            drone.send_rc_control(0, STEP, 0, 0)
        elif k == "s":
            drone.send_rc_control(0, -STEP, 0, 0)
        elif k == "a":
            drone.send_rc_control(-STEP, 0, 0, 0)
        elif k == "d":
            drone.send_rc_control(STEP, 0, 0, 0)
        elif name == "up":
            drone.send_rc_control(0, 0, STEP, 0)
        elif name == "down":
            drone.send_rc_control(0, 0, -STEP, 0)
        elif name == "left":
            drone.send_rc_control(0, 0, 0, -STEP)
        elif name == "right":
            drone.send_rc_control(0, 0, 0, STEP)
        elif name == "space":
            drone.send_rc_control(0, 0, 0, 0)
            print("hover (RC zeroed)")

    def on_release(key):
        # Stop motion when a motion key is released.
        name = getattr(key, "name", None)
        try:
            k = key.char.lower() if key.char else None
        except AttributeError:
            k = None
        if (k in ("w", "s", "a", "d") or name in ("up", "down", "left", "right")) and state["flying"]:
            drone.send_rc_control(0, 0, 0, 0)

    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    finally:
        if state["flying"]:
            try:
                drone.land()
            except Exception:
                pass
        try:
            drone.shutdown()
        except Exception:
            pass
        print("Keyboard control exited.")


if __name__ == "__main__":
    main()
