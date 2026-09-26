# Version pins

| Package | Pin | Why |
|---|---|---|
| robotpy | 2027.0.0a6.post1 | Last alpha with the camelCase wpilib API that phoenix6 26.50.0a1 was built against |
| phoenix6 | 26.50.0a1 | Only SystemCore-capable Phoenix 6 Python release (aarch64 wheel) as of 2026-09 |
| pygame-ce (dev only) | 2.5.8 | SDL 2.32 for `sim/gamepad_bridge.py`: reads USB gamepads the sim GUI can't (wired Xbox Series on macOS). Never deployed |

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
| `CommandXboxController` | `wpilib.Gamepad` + `Trigger(pad.getSouthFaceButton)` (not `CommandNiDsXboxController`: old NI DS indices, wrong right stick/bumpers in sim) |
| `robotInit()` | `__init__()` |
| `from pyfrc.tests import *` | `from wpilib.testing.robot_tests import *` |

## Testing gotchas (phoenix6 26.50.0a1 + wpilib.testing)

- **Sim clock.** `phoenix6.utils.get_current_time_seconds()` is wall-clock in
  simulation, but `wpilib.Notifier` fires on HAL sim time. The Tuner X template's
  `_sim_periodic` computes `delta_time` from the Phoenix clock, so headless tests
  that fast-forward time (`control.step_timing`) under-integrate physics by
  whatever ratio the machine runs at (we measured 0.43 m/s for a 1 m/s command).
  `subsystems/drivetrain.py` uses `wpilib.Timer.getTimestamp()` instead. Keep that
  edit when regenerating from Tuner X.
- **One robot per process.** `phoenix6.wpiutils.auto_feed_enable.AutoFeedEnable` is
  a process-wide singleton whose `Notifier` is destroyed by the test harness's
  `hal.simulation.resetGlobalHandles()` teardown. A second robot booted in the same
  process never gets `feed_enable()` and every TalonFX outputs 0 V. `robotpy test`
  isolates each test in its own process by default — do **not** use
  `--no-isolation`, and do not pass test file paths as arguments (the isolated
  worker re-collects the whole file in one process); select tests with `-k`.
- `control.step_timing(seconds=s)` steps `s + 0.2` (loop condition is
  `tm < seconds + 0.01`). Don't rely on it for exact durations.
