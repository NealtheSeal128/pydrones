"""Gamepad / joystick control.

    python control/gamepad_control.py

Mapping (Xbox/PlayStation via pygame):
  A/Cross take off | B/Circle land | Y/Triangle hover | Start quit
  Left stick X/Y: left-right / forward-back
  Right stick X: yaw, Right stick Y: up-down (inverted: push up = ascend)

Requires: pip install pygame. Deadzone applied so idle sticks send zero.
"""

import sys
import time

sys.path.insert(0, ".")

from pysimverse import Drone

from utils.drone_base import RC_FRAME

DEADZONE = 0.15
SCALE = 100


def _axis(value):
    if abs(value) < DEADZONE:
        return 0
    return int(max(-1.0, min(1.0, value)) * SCALE)


def main():
    try:
        import pygame
    except ImportError:
        print("pygame not installed. Run: pip install pygame")
        raise SystemExit(1)

    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("No gamepad detected. Connect one and retry.")
        raise SystemExit(1)
    pad = pygame.joystick.Joystick(0)
    pad.init()
    print(f"Gamepad: {pad.get_name()}")

    drone = Drone()
    drone.connect()
    flying = False
    print("A take off | B land | Y hover | Start quit")

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    btn = event.button
                    if btn == 0 and not flying:     
                        drone.take_off()
                        flying = True
                    elif btn == 1 and flying:     
                        drone.land()
                        flying = False
                    elif btn == 3 and flying:     
                        drone.send_rc_control(0, 0, 0, 0)
                        print("hover")
                    elif btn == 7:         
                        print("Quitting.")
                        return
            if flying and pad.get_numaxes() >= 4:
                lr = _axis(pad.get_axis(0))
                fb = _axis(-pad.get_axis(1))
                yaw = _axis(pad.get_axis(2))
                ud = _axis(-pad.get_axis(3))
                drone.send_rc_control(lr, fb, ud, yaw)
            time.sleep(RC_FRAME)
    finally:
        if flying:
            try:
                drone.land()
            except Exception:
                pass
        try:
            drone.shutdown()
        except Exception:
            pass
        pygame.quit()


if __name__ == "__main__":
    main()
