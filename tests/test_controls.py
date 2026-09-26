import math

import pytest

from controls import DriverControls


def make(slew=1e9):
    # Huge slew rate = effectively no limiting, so shape tests see the raw mapping.
    return DriverControls(
        max_speed_mps=4.0, max_angular_rate_rps=math.pi, deadband=0.1, slew_rate_per_s=slew
    )


def test_inside_deadband_is_zero():
    v = make().compute(left_x=0.05, left_y=-0.05, right_x=0.09)
    assert v.vx == 0 and v.vy == 0 and v.omega == 0


def test_full_forward_stick_is_max_forward_speed():
    v = make().compute(left_x=0.0, left_y=-1.0, right_x=0.0)  # Xbox: pushing up is -1
    assert v.vx == pytest.approx(4.0)
    assert v.vy == pytest.approx(0.0)


def test_stick_right_is_negative_vy_and_stick_right_rotation_is_clockwise():
    v = make().compute(left_x=1.0, left_y=0.0, right_x=1.0)
    assert v.vy == pytest.approx(-4.0)
    assert v.omega == pytest.approx(-math.pi)


def test_input_is_squared_for_fine_control():
    v = make().compute(left_x=0.0, left_y=-0.5, right_x=0.0)
    # deadband rescales 0.5 -> (0.5-0.1)/(1-0.1) = 0.444..., squared = 0.1975.., x 4 m/s
    expected = ((0.5 - 0.1) / 0.9) ** 2 * 4.0
    assert v.vx == pytest.approx(expected, rel=1e-6)


def test_slow_mode_halves_everything():
    fast = make().compute(0.0, -1.0, 1.0)
    slow = make().compute(0.0, -1.0, 1.0, slow=True)
    assert slow.vx == pytest.approx(fast.vx * 0.5)
    assert slow.omega == pytest.approx(fast.omega * 0.5)


def test_slew_limits_acceleration():
    c = DriverControls(
        max_speed_mps=4.0, max_angular_rate_rps=math.pi, deadband=0.1, slew_rate_per_s=2.0
    )
    c.reset()
    first = c.compute(0.0, -1.0, 0.0)
    # SlewRateLimiter uses wall-clock time between calls; immediately after reset the
    # allowed change is ~0, so the first output is far below max.
    assert first.vx < 1.0
