"""Map Xbox stick positions to field-relative chassis velocities.

Pure logic: no hardware, no scheduler. The RobotContainer feeds raw axis values in
and passes the result to Drivetrain.drive_field_centric().
"""

from wpimath import ChassisVelocities, SlewRateLimiter, applyDeadband


class DriverControls:
    SLOW_MODE_SCALE = 0.5

    def __init__(
        self,
        max_speed_mps: float,
        max_angular_rate_rps: float,
        deadband: float = 0.1,
        slew_rate_per_s: float = 4.0,
    ) -> None:
        self._max_speed = max_speed_mps
        self._max_omega = max_angular_rate_rps
        self._deadband = deadband
        self._slew_rate = slew_rate_per_s
        self._vx_limiter = SlewRateLimiter(slew_rate_per_s)
        self._vy_limiter = SlewRateLimiter(slew_rate_per_s)
        self._omega_limiter = SlewRateLimiter(slew_rate_per_s)

    def reset(self) -> None:
        """Forget previous stick state so re-enabling doesn't lurch."""
        for limiter in (self._vx_limiter, self._vy_limiter, self._omega_limiter):
            limiter.reset(0.0)

    def _shape(self, raw: float) -> float:
        """Deadband (rescaled) then square, keeping sign. Output in [-1, 1]."""
        x = applyDeadband(raw, self._deadband)
        return x * abs(x)

    def compute(
        self, left_x: float, left_y: float, right_x: float, slow: bool = False
    ) -> ChassisVelocities:
        scale = self.SLOW_MODE_SCALE if slow else 1.0
        # Xbox: forward stick is -Y; right stick is +X. WPILib: +vx forward, +vy left, +omega CCW.
        vx = self._shape(-left_y) * self._max_speed * scale
        vy = self._shape(-left_x) * self._max_speed * scale
        omega = self._shape(-right_x) * self._max_omega * scale
        return ChassisVelocities(
            self._vx_limiter.calculate(vx),
            self._vy_limiter.calculate(vy),
            self._omega_limiter.calculate(omega),
        )
