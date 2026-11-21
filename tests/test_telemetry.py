import ntcore


def test_field_and_pose_are_published(control, robot):
    """Field2d (sim GUI) and the pose struct (AdvantageScope) appear on NetworkTables."""
    with control.run_robot():
        control.step_timing(seconds=0.5, autonomous=False, enabled=False)
        inst = ntcore.NetworkTableInstance.get_default()
        names = {t.get_name() for t in inst.get_topics()}
    assert "/Tunables/Field/Robot" in names
    assert "/Robot/Pose" in names
