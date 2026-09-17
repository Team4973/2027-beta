# Version pins

| Package | Pin | Why |
|---|---|---|
| robotpy | 2027.0.0a6.post1 | Last alpha with the camelCase wpilib API that phoenix6 26.50.0a1 was built against |
| phoenix6 | 26.50.0a1 | Only SystemCore-capable Phoenix 6 Python release (aarch64 wheel) as of 2026-09 |

## Verified 2026-09-12

On macOS, a copy of `2026-rebuilt`'s drivetrain runs in the Phoenix 6 swerve sim
and all four `wpilib.testing.robot_tests` pass on this pair.

`robotpy==2027.0.0a7` **does not work**: it renamed the Python API to snake_case
(`RobotBase.is_simulation`, `Rotation2d.from_degrees`, `wpimath.inches_to_meters`)
and phoenix6 26.50.0a1 still calls `RobotBase.isSimulation()`. `photonlibpy
2027.0.0a2` also fails to import on a7 (`Timer.getMonotonicTimestamp`).

## How to bump

1. Branch. Change the pin in `pyproject.toml` (both `[project]` and `[tool.robotpy]`).
2. `uv lock && uv run python -m robotpy test`.
3. If phoenix6 imports and the drivetrain test passes, update this file and open a PR.
4. If the bump crosses into alpha-7+, budget a full snake_case rename of every
   `wpilib`/`wpimath`/`commands2` call (see roadmap Phase 8).

## alpha-6 API cheat sheet (differs from 2026)

| 2026 | 2027 alpha-6 |
|---|---|
| `from wpimath.geometry import Pose2d` | `from wpimath import Pose2d` |
| `ChassisSpeeds` | `ChassisVelocities` |
| `SwerveModuleState` | `SwerveModuleVelocity` |
| `DriverStation.getAlliance()` | `MatchState.getAlliance()` |
| `DriverStation.Alliance.kRed` | `Alliance.RED` |
| `DriverStation.isDisabled()` | `RobotState.isDisabled()` |
| `CommandXboxController` | `CommandNiDsXboxController` |
| `robotInit()` | `__init__()` |
| `from pyfrc.tests import *` | `from wpilib.testing.robot_tests import *` |
