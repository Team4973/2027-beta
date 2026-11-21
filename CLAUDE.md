# CLAUDE.md

RobotPy (Python WPILib) project for FRC Team 4973's 2027 robot on the Limelight SystemCore.

## Commands

    uv run python -m robotpy sim      # simulator GUI
    uv run python -m robotpy test     # all tests
    uv run pytest tests/test_controls.py -q   # one fast pure-logic file (no robot fixtures)
    uv run python -m robotpy test -- -k drivetrain   # select robot tests with -k, never by path
    uv run ruff check . && uv run ruff format .
    uv run python -m robotpy deploy   # to SystemCore (needs robot network)

## Rules

- Version pins are exact and documented in `docs/versions.md`. Do not bump them in a feature PR.
- Since alpha-7 the whole API is snake_case (`is_disabled`, `Rotation2d.from_degrees`,
  `pose.x` is a property). `from wpimath import Pose2d` — there is no `wpimath.geometry`.
  `ChassisVelocities`, not `ChassisSpeeds`. No SmartDashboard: use `tunables` / NT struct topics.
- Physical numbers (frame, mass, MOI, camera transforms) live only in `constants/robot_physical.py`.
- `constants/tuner_constants.py` is Tuner X output: regenerate, don't hand-edit (except the
  `robot_physical` import for module positions).
- Only `subsystems/drivetrain.py` and `subsystems/vision.py` import vendor libraries.
- If you change a controller binding, update `docs/controls.md` in the same PR.
- Tests use `wpilib.testing` (fixtures `control`, `robot`). pyfrc no longer exists.
- Robot tests must run one-per-process (`robotpy test` default). Never `--no-isolation`; see `docs/versions.md`.

## Layout

    robot.py            TimedCommandRobot entry
    robotcontainer.py   subsystems + bindings
    controls.py         DriverControls: sticks -> ChassisVelocities
    constants/          robot_physical.py (hand-edited), tuner_constants.py (generated)
    subsystems/         drivetrain.py (Phoenix 6 swerve wrapper)
    sim/                field.py (Field2d + NT pose publisher)
    tests/              pytest
    docs/               versions.md, controls.md
