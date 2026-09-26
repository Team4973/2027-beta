import math

from constants import robot_physical as rp
from constants.tuner_constants import TunerConstants


def _pos(module):
    return (module.location_x, module.location_y)


def test_module_positions_match_robot_physical():
    for name, module in {
        "front_left": TunerConstants.front_left,
        "front_right": TunerConstants.front_right,
        "back_left": TunerConstants.back_left,
        "back_right": TunerConstants.back_right,
    }.items():
        expected = rp.MODULE_POSITIONS_M[name]
        actual = _pos(module)
        assert math.isclose(actual[0], expected[0], abs_tol=1e-3), name
        assert math.isclose(actual[1], expected[1], abs_tol=1e-3), name


def test_speed_at_12v_matches_robot_physical():
    assert math.isclose(TunerConstants.speed_at_12_volts, rp.MAX_SPEED_MPS, rel_tol=1e-6)
