"""Drive the simulated robot through port 0 with the 2027 gamepad layout.

GamepadSim writes axes/buttons at the indices the sim GUI and SystemCore DS use
(wpilib.Gamepad.Axis / .Button), so these catch a wrong controller class.
"""

from wpilib.simulation import GamepadSim
from wpimath import Pose2d

from constants import robot_physical as rp


def _connect_gamepad() -> GamepadSim:
    pad = GamepadSim(0)
    pad.setAxesMaximumIndex(6)
    pad.setAxesAvailable(0x3F)
    pad.setButtonsMaximumIndex(26)
    pad.setButtonsAvailable((1 << 26) - 1)
    pad.notifyNewData()
    return pad


def test_left_stick_forward_drives_forward(control, robot):
    with control.run_robot():
        control.step_timing(seconds=0.5, autonomous=False, enabled=False)
        dt = robot.container.drivetrain
        dt.reset_pose(Pose2d())
        pad = _connect_gamepad()
        pad.setLeftY(-1.0)  # pushed away from the driver
        pad.notifyNewData()
        control.step_timing(seconds=1.0, autonomous=False, enabled=True)
        end = dt.get_pose()

    assert end.X() > 1.0, f"expected forward travel, got x={end.X():.2f} m"
    assert abs(end.rotation().degrees()) < 5


def test_right_stick_right_rotates_clockwise(control, robot):
    with control.run_robot():
        control.step_timing(seconds=0.5, autonomous=False, enabled=False)
        dt = robot.container.drivetrain
        dt.reset_pose(Pose2d())
        pad = _connect_gamepad()
        pad.setRightX(1.0)
        pad.notifyNewData()
        control.step_timing(seconds=1.0, autonomous=False, enabled=True)
        end = dt.get_pose()

    assert end.rotation().degrees() < -20, f"expected clockwise, got {end.rotation()}"


def test_left_bumper_is_slow_mode(control, robot):
    with control.run_robot():
        control.step_timing(seconds=0.5, autonomous=False, enabled=False)
        dt = robot.container.drivetrain
        dt.reset_pose(Pose2d())
        pad = _connect_gamepad()
        pad.setLeftY(-1.0)
        pad.setLeftBumperButton(True)
        pad.notifyNewData()
        # Long enough for the 4 m/s^2 slew limit to settle at the slow-mode speed.
        control.step_timing(seconds=1.5, autonomous=False, enabled=True)
        slow = dt.get_chassis_velocities().vx

    target = rp.MAX_SPEED_MPS * robot.container.controls.SLOW_MODE_SCALE
    assert abs(slow - target) < 0.4, f"expected ~{target:.2f} m/s in slow mode, got {slow:.2f}"


def test_gamepad_bridge_message_drives_robot(control, robot):
    """A message from the SDL helper, written to port 0, drives like a real gamepad."""
    from sim.gamepad_bridge import GamepadBridge

    with control.run_robot():
        control.step_timing(seconds=0.5, autonomous=False, enabled=False)
        dt = robot.container.drivetrain
        dt.reset_pose(Pose2d())
        # SDL: left stick pushed away (-y), right stick right (+x).
        GamepadBridge().write(
            {"name": "Controller", "axes": [0, -32768, 32767, 0, 0, 0], "buttons": 0}
        )
        control.step_timing(seconds=1.0, autonomous=False, enabled=True)
        end = dt.get_pose()

    assert end.X() > 0.5
    assert end.rotation().degrees() < -20
