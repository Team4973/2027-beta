"""Entry point. RobotPy looks for a RobotBase subclass in this file."""

import commands2


class MyRobot(commands2.TimedCommandRobot):
    """Command-based robot. The scheduler runs in robotPeriodic via TimedCommandRobot.

    2027 removed robotInit(); do setup in __init__.
    """

    def __init__(self) -> None:
        super().__init__()
        self.autonomous_command: commands2.Command | None = None

    def autonomousInit(self) -> None:
        if self.autonomous_command is not None:
            self.autonomous_command.schedule()

    def teleopInit(self) -> None:
        if self.autonomous_command is not None:
            self.autonomous_command.cancel()
