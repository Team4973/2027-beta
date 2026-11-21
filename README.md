# 2027-beta

Team 4973's 2027 season robot code: RobotPy on the Limelight SystemCore.
A 22" four-module swerve drive base. See `docs/versions.md` for the pins.

## Setup (once)

    curl -LsSf https://astral.sh/uv/install.sh | sh      # macOS/Linux
    # Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

## Run the simulator

    uv run python -m robotpy sim

1. Plug in an Xbox controller **before** launching.
2. In the sim window, open **System Joysticks** — your controller is listed there.
3. Drag it into slot **0** in the **Joysticks** panel.
4. In **Robot State**, click **Teleoperated**.
5. Open the **Field** widget (NetworkTables `/Tunables/Field`) to see the robot on the field.
   Drive with the left stick, rotate with the right stick. Controls: `docs/controls.md`.

macOS: if the controller doesn't appear, grant the terminal Bluetooth/Input Monitoring
permission in System Settings → Privacy & Security, then relaunch.

**Wired Xbox Series controller on macOS:** the sim GUI lists it as "Controller" but reads
no axes or buttons (it's missing from the GUI's built-in mapping table). The sim reads it
through SDL instead (`sim/gamepad_bridge.py`) and feeds it into port 0 automatically.
Leave slot 0 in the **Joysticks** panel **empty**, and skip steps 2–3.
No controller? Map the **Keyboard 0** virtual joystick into slot 0 instead (WASD + arrows).

## Tests

    uv run python -m robotpy test          # everything (~90 s)
    uv run pytest tests/test_controls.py   # one fast file

## Deploy (Phase 6, needs a SystemCore)

    uv run python -m robotpy sync
    uv run python -m robotpy deploy

## Contributing

Branch from `main`, open a PR, CI must pass, one review. If you change a controller
binding, update `docs/controls.md`. Conventions for AI assistants: `CLAUDE.md`.
