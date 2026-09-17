"""Every physical number about the robot, in one place.

Hand-edited. Update from CAD (mass, MOI, dimensions) and from SysId
(see docs/sysid-procedure.md, Phase 7). Nothing else in the codebase may
hardcode a physical quantity.

Units are SI (meters, kilograms, seconds, radians) unless the name says otherwise.
"""

import math

INCH = 0.0254

# --- Frame and modules -------------------------------------------------------
FRAME_SIDE_M = 22 * INCH
"""Outside dimension of the square frame perimeter (no bumpers)."""

MODULE_INSET_M = 2.75 * INCH
"""Distance from the frame edge to the wheel contact point for MK4i-class modules."""

MODULE_HALF_SPACING_M = (FRAME_SIDE_M - 2 * MODULE_INSET_M) / 2
"""Half the wheel center-to-center distance; module x/y offsets are +/- this."""

MODULE_POSITIONS_M: dict[str, tuple[float, float]] = {
    # WPILib convention: +x forward, +y left, origin at robot center.
    "front_left": (MODULE_HALF_SPACING_M, MODULE_HALF_SPACING_M),
    "front_right": (MODULE_HALF_SPACING_M, -MODULE_HALF_SPACING_M),
    "back_left": (-MODULE_HALF_SPACING_M, MODULE_HALF_SPACING_M),
    "back_right": (-MODULE_HALF_SPACING_M, -MODULE_HALF_SPACING_M),
}

BUMPER_THICKNESS_M = 3.25 * INCH

# --- Mass properties (PLACEHOLDERS until CAD/scale numbers exist) ------------
ROBOT_MASS_KG = 45.0
"""Drive base + bumpers + battery + electronics. Weigh the robot in Phase 7."""

ROBOT_MOI_KG_M2 = ROBOT_MASS_KG * FRAME_SIDE_M**2 / 6 * 1.3
"""Yaw inertia. Uniform-plate estimate x1.3 for mass concentrated at the corners.
Replace with the Onshape mass-properties value (docs/cad-export.md)."""

# --- Speed limits used by teleop scaling -------------------------------------
MAX_SPEED_MPS = 4.42
"""Free speed at 12 V from the 2026 Tuner X constants; re-measure after SysId."""

MAX_ANGULAR_RATE_RPS = 0.75 * 2 * math.pi
"""Three-quarters of a rotation per second; a comfortable teleop cap."""
