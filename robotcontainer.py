"""Declares subsystems, controller bindings, and the default drive command."""

import commands2
from commands2.button import Trigger
from wpilib import Gamepad, RobotState

from constants import robot_physical as rp
from constants.tuner_constants import TunerConstants
from controls import DriverControls
from sim.field import FieldPublisher
from sim.gamepad_bridge import GamepadBridge
from subsystems.drivetrain import Drivetrain


class RobotContainer:
    def __init__(self) -> None:
        self.drivetrain: Drivetrain = TunerConstants.create_drivetrain()
        self.controls = DriverControls(
            max_speed_mps=rp.MAX_SPEED_MPS,
            max_angular_rate_rps=rp.MAX_ANGULAR_RATE_RPS,
        )
        # Gamepad, not NiDsXboxController: the 2027 sim GUI reports the SDL gamepad layout
        # (right stick X = axis 2, left bumper = button 9). NiDs indices are the old NI DS ones.
        self.gamepad = Gamepad(0)
        self.field = FieldPublisher()
        self.gamepad_bridge: GamepadBridge | None = None
        if GamepadBridge.should_start():
            self.gamepad_bridge = GamepadBridge()
            self.gamepad_bridge.start()

        # Tests set this to (vx, vy, omega) to drive without a joystick. None in normal use.
        self.test_hook_command_velocity: tuple[float, float, float] | None = None

        self._configure_bindings()

    # -- bindings ----------------------------------------------------------
    def _configure_bindings(self) -> None:
        # Default: field-centric drive from the sticks. Documented in docs/controls.md.
        self.drivetrain.set_default_command(
            self.drivetrain.run(self._drive_from_sticks).with_name("DriveFromSticks")
        )
        # A (hold): brake in an X.
        Trigger(self.gamepad.get_face_down_button).while_true(
            self.drivetrain.run(self.drivetrain.brake).with_name("Brake")
        )
        # X: make "forward" the way the robot is currently facing.
        Trigger(self.gamepad.get_face_left_button).on_true(
            self.drivetrain.run_once(self.drivetrain.seed_field_centric).with_name("ResetHeading")
        )
        # Reset slew limiters whenever we go from disabled to enabled.
        Trigger(lambda: not RobotState.is_disabled()).on_true(
            commands2.cmd.run_once(self.controls.reset).ignoring_disable(True)
        )

    def _drive_from_sticks(self) -> None:
        if self.test_hook_command_velocity is not None:
            vx, vy, omega = self.test_hook_command_velocity
            self.drivetrain.drive_field_centric(vx, vy, omega)
            return
        v = self.controls.compute(
            left_x=self.gamepad.get_left_x(),
            left_y=self.gamepad.get_left_y(),
            right_x=self.gamepad.get_right_x(),
            slow=self.gamepad.get_left_bumper_button(),
        )
        self.drivetrain.drive_field_centric(v.vx, v.vy, v.omega)

    # -- periodic ----------------------------------------------------------
    def update_telemetry(self) -> None:
        self.field.update(self.drivetrain.get_pose())

    def update_sim_gamepad(self) -> None:
        if self.gamepad_bridge is not None:
            self.gamepad_bridge.update()

    # -- autonomous --------------------------------------------------------
    def get_autonomous_command(self) -> commands2.Command | None:
        """Phase 3 replaces this with a chooser. For now: nothing."""
        return None
