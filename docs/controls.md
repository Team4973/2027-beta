# Driver controls (Xbox, port 0)

| Control | Action |
|---|---|
| Left stick | Translate, field-centric (push away from you = away from the driver station) |
| Right stick X | Rotate (push right = clockwise) |
| Left bumper (hold) | Slow mode (50%) |
| A (hold) | Brake: wheels in an X |
| X | Reset field-centric heading (robot's current facing becomes "forward") |

Read through `wpilib.Gamepad` (2027 SDL layout; A = south face, X = west face).

Stick shaping: 10% deadband, squared response, 4 m/s² slew limit. See `controls.py`.

**If you change a binding, update this table in the same PR.**
