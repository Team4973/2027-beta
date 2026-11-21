"""Entry point. RobotPy looks for a RobotBase subclass in this file."""

import commands2

from robotcontainer import RobotContainer


class MyRobot(commands2.TimedCommandRobot):
    """Command-based robot. The scheduler runs in robot_periodic via TimedCommandRobot.

    2027 removed robotInit(); do setup in __init__.
    """

    def __init__(self) -> None:
        super().__init__()
        self.container = RobotContainer()
        self.autonomous_command: commands2.Command | None = None

    def robot_periodic(self) -> None:
        # Sim-only USB gamepad feed; must land right before the scheduler reads the sticks.
        self.container.update_sim_gamepad()
        super().robot_periodic()  # runs the CommandScheduler
        self.container.update_telemetry()

    def autonomous_init(self) -> None:
        self.autonomous_command = self.container.get_autonomous_command()
        if self.autonomous_command is not None:
            self.autonomous_command.schedule()

    def teleop_init(self) -> None:
        if self.autonomous_command is not None:
            self.autonomous_command.cancel()
