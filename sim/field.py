"""Publish the robot pose for the sim GUI (Field2d) and AdvantageScope (NT4 struct)."""

import ntcore
import tunables
import wpilib
from wpimath import Pose2d


class FieldPublisher:
    def __init__(self) -> None:
        self._field = wpilib.Field2d()
        # SmartDashboard is gone in alpha-7+; Field2d is now a complex tunable.
        tunables.publish("Field", self._field)
        self._pose_pub = (
            ntcore.NetworkTableInstance.get_default()
            .get_struct_topic("/Robot/Pose", Pose2d)
            .publish()
        )

    def update(self, pose: Pose2d) -> None:
        self._field.set_robot_pose(pose)
        self._pose_pub.set(pose)
