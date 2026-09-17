# CLAUDE.md

RobotPy (Python WPILib) project for FRC Team 4973's 2027 robot on the Limelight SystemCore.

## Commands

    uv run python -m robotpy sim      # simulator GUI
    uv run python -m robotpy test     # all tests
    uv run pytest tests/test_controls.py -q   # one fast test file
    uv run ruff check . && uv run ruff format .
    uv run python -m robotpy deploy   # to SystemCore (needs robot network)

## Rules

- Version pins are exact and documented in `docs/versions.md`. Do not bump them in a feature PR.
- The alpha-6 API is camelCase for wpilib (`isDisabled`), snake_case for phoenix6 (`get_state`).
  `from wpimath import Pose2d` — there is no `wpimath.geometry`. `ChassisVelocities`, not `ChassisSpeeds`.
- Physical numbers (frame, mass, MOI, camera transforms) live only in `constants/robot_physical.py`.
- `constants/tuner_constants.py` is Tuner X output: regenerate, don't hand-edit (except the
  `robot_physical` import for module positions).
- Only `subsystems/drivetrain.py` and `subsystems/vision.py` import vendor libraries.
- If you change a controller binding, update `docs/controls.md` in the same PR.
- Tests use `wpilib.testing` (fixtures `control`, `robot`). pyfrc no longer exists.

## Layout

    robot.py            TimedCommandRobot entry
    robotcontainer.py   subsystems + bindings
    controls.py         DriverControls: sticks -> ChassisVelocities
    constants/          robot_physical.py (hand-edited), tuner_constants.py (generated)
    subsystems/         drivetrain.py (Phoenix 6 swerve wrapper)
    sim/                field.py (Field2d + NT pose publisher)
    tests/              pytest
    docs/               versions.md, controls.md
