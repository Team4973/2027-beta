import math

from constants import robot_physical as rp


def test_frame_is_22_inches():
    assert math.isclose(rp.FRAME_SIDE_M, 22 * 0.0254, rel_tol=1e-9)


def test_module_half_spacing_derived_from_frame_and_inset():
    # 22" frame, MK4i-class modules sit 2.75" in from the frame edge -> 16.5" center-to-center
    expected_half = (22 - 2 * 2.75) / 2 * 0.0254
    assert math.isclose(rp.MODULE_HALF_SPACING_M, expected_half, rel_tol=1e-9)


def test_module_positions_are_symmetric_and_named():
    h = rp.MODULE_HALF_SPACING_M
    assert rp.MODULE_POSITIONS_M == {
        "front_left": (h, h),
        "front_right": (h, -h),
        "back_left": (-h, h),
        "back_right": (-h, -h),
    }


def test_mass_and_moi_are_positive_and_moi_is_plausible_for_a_box():
    assert rp.ROBOT_MASS_KG > 0
    # Uniform square plate: I = m * s^2 / 6. Real robots land within ~0.5x-2x of this.
    plate = rp.ROBOT_MASS_KG * rp.FRAME_SIDE_M**2 / 6
    assert 0.5 * plate < rp.ROBOT_MOI_KG_M2 < 2.0 * plate
