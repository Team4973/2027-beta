"""Drive the simulated swerve forward and check odometry moves."""

import math

from wpimath import Pose2d


def test_field_centric_drive_moves_robot(control, robot):
    with control.run_robot():
        # Let the robot construct and the Phoenix sim thread start.
        control.step_timing(seconds=0.5, autonomous=False, enabled=False)

        dt = robot.container.drivetrain
        dt.reset_pose(Pose2d())
        control.step_timing(seconds=0.2, autonomous=False, enabled=False)
        start = dt.get_pose()

        # Enable teleop with no controller input; command 1 m/s forward directly.
        robot.container.test_hook_command_velocity = (1.0, 0.0, 0.0)
        control.step_timing(seconds=2.0, autonomous=False, enabled=True)
        end = dt.get_pose()

    moved = end.x - start.x
    assert moved > 1.5, f"expected >=1.5 m forward in 2 s at 1 m/s, got {moved:.2f} m"
    assert abs(end.y - start.y) < 0.1
    assert abs(end.rotation().radians()) < math.radians(5)
