"""Feed a USB gamepad into port 0 when the sim GUI can't read it.

The 2027 sim GUI only reads controllers listed in its built-in GLFW mapping table.
The wired Xbox Series controller on macOS (045e:0b12) isn't listed, so it shows up
with zero axes and buttons. SDL can read it, so a helper process polls it with
pygame-ce and the robot writes the values into port 0 each loop.

SDL has to run on a process's main thread on macOS, and robot code doesn't, hence the
subprocess. SDL's GameController axis/button order matches wpilib.Gamepad index for
index, so values copy straight across.

Sim only: the robot starts this only when the GUI is loaded, never under
`robotpy test`. If pygame-ce is missing or no controller is plugged in, port 0 is
left to the GUI (e.g. Keyboard 0).
"""

import json
import os
import subprocess
import sys
import threading

NUM_AXES = 6  # left x/y, right x/y, left/right trigger
NUM_BUTTONS = 21  # south, east, west, north, ... touchpad
_SDL_AXIS_MAX = 32767
_TRIGGER_AXES = (4, 5)


def sdl_axes_to_wpilib(raw: list[int]) -> list[float]:
    """SDL ints (-32768..32767, triggers 0..32767) -> sticks [-1, 1], triggers [0, 1]."""
    out = []
    for i, v in enumerate(raw[:NUM_AXES]):
        lo = 0.0 if i in _TRIGGER_AXES else -1.0
        out.append(max(lo, min(1.0, v / _SDL_AXIS_MAX)))
    return out


class GamepadBridge:
    def __init__(self, port: int = 0) -> None:
        self._port = port
        self._latest: dict | None = None
        self._owns_port = False
        self._proc: subprocess.Popen | None = None

    @staticmethod
    def should_start() -> bool:
        """Only under `robotpy sim` with the GUI; tests never load halsim_gui."""
        return "halsim_gui" in sys.modules

    def start(self) -> None:
        self._proc = subprocess.Popen(
            [sys.executable, os.path.abspath(__file__)],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        threading.Thread(target=self._read_loop, daemon=True, name="GamepadBridge").start()

    def _read_loop(self) -> None:
        assert self._proc is not None and self._proc.stdout is not None
        for line in self._proc.stdout:
            try:
                self._latest = json.loads(line)
            except json.JSONDecodeError:
                continue

    def update(self) -> None:
        """Call at the start of robotPeriodic. Writes port 0 only while a controller is present.

        Rewrites every loop, not just on change, because the GUI rewrites slot 0 on its own
        frame timer. Writing just before the scheduler reads the sticks wins that race.
        Leave slot 0 empty in the GUI's Joysticks panel so there is nothing to race.
        """
        msg = self._latest
        if msg is None:
            return
        if msg.get("name") is None:
            if self._owns_port:  # controller unplugged: clear once, then hand back to the GUI
                self.write(msg)
                self._owns_port = False
            return
        self._owns_port = True
        self.write(msg)

    def write(self, msg: dict) -> None:
        from wpilib.simulation import GamepadSim

        pad = GamepadSim(self._port)
        if msg.get("name") is None:
            pad.setAxesAvailable(0)
            pad.setButtonsAvailable(0)
            pad.notifyNewData()
            return
        pad.setName(msg["name"])
        pad.setAxesMaximumIndex(NUM_AXES)
        pad.setAxesAvailable((1 << NUM_AXES) - 1)
        pad.setButtonsMaximumIndex(NUM_BUTTONS)
        pad.setButtonsAvailable((1 << NUM_BUTTONS) - 1)
        for i, v in enumerate(sdl_axes_to_wpilib(msg["axes"])):
            pad.setRawAxis(i, v)
        for i in range(NUM_BUTTONS):
            pad.setRawButton(i, bool(msg["buttons"] >> i & 1))
        pad.notifyNewData()


def _reader_main() -> None:
    """Helper process: poll the first SDL game controller, print JSON on every change."""
    import time

    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    # macOS only delivers controller input to the foreground app without this.
    os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
    import pygame
    from pygame._sdl2 import controller

    pygame.init()
    controller.init()
    parent = os.getppid()
    pad = None
    last = None
    while os.getppid() == parent:
        pygame.event.pump()
        if pad is None:
            for i in range(pygame.joystick.get_count()):
                if controller.is_controller(i):
                    pad = controller.Controller(i)
                    break
        if pad is not None and not pad.attached():
            pad = None
        if pad is None:
            msg = {"name": None}
        else:
            msg = {
                "name": pad.name,
                "axes": [pad.get_axis(a) for a in range(NUM_AXES)],
                "buttons": sum(pad.get_button(b) << b for b in range(NUM_BUTTONS)),
            }
        if msg != last:
            try:
                print(json.dumps(msg), flush=True)
            except BrokenPipeError:
                return
            last = msg
        time.sleep(0.005)


if __name__ == "__main__":
    _reader_main()
