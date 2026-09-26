"""Pure logic for the sim gamepad bridge (no robot fixtures)."""

import pytest

from sim.gamepad_bridge import GamepadBridge, sdl_axes_to_wpilib


def test_sticks_scale_to_unit_range():
    assert sdl_axes_to_wpilib([32767, -32768, 0, 16384, 0, 0])[:4] == pytest.approx(
        [1.0, -1.0, 0.0, 0.5], abs=1e-4
    )


def test_triggers_are_zero_to_one():
    assert sdl_axes_to_wpilib([0, 0, 0, 0, 0, 32767])[4:] == pytest.approx([0.0, 1.0])


def test_not_started_without_sim_gui():
    assert not GamepadBridge.should_start()
