"""Publish the robot pose for the sim GUI (Field2d) and AdvantageScope (NT4 struct)."""

import ntcore
import wpilib
from wpimath import Pose2d


class FieldPublisher:
    def __init__(self) -> None:
        self._field = wpilib.Field2d()
        # The halsim GUI's Field2d widget reads SmartDashboard/Field. (SmartDashboard is
        # removed in alpha-7; the struct topic below is the long-term path.)
        wpilib.SmartDashboard.putData("Field", self._field)
        self._pose_pub = (
            ntcore.NetworkTableInstance.getDefault().getStructTopic("/Robot/Pose", Pose2d).publish()
        )

    def update(self, pose: Pose2d) -> None:
        self._field.setRobotPose(pose)
        self._pose_pub.set(pose)
