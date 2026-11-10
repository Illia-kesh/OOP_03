"""Task 3.6 - Thermostat (chapter 3: protecting object state)."""

class Thermostat:
    """Thermostat whose target temperature is clamped to [min_t, max_t]."""

    def __init__(self, min_t, max_t, target=None):
        """Create a thermostat with a allowed range and an optional target."""
        if min_t > max_t:
            raise ValueError("min_t must not be greater than max_t")
        self._min_t = min_t
        self._max_t = max_t
        self._target = min_t
        self.target = min_t if target is None else target

    @property
    def target(self):
        """Target temperature (always inside the allowed range)."""
        return self._target

    @target.setter
    def target(self, value):
        """Set the target; out-of-range values are clamped, no error raised."""
        self._target = max(self._min_t, min(self._max_t, value))

    def heating_needed(self, current):
        """Return True if the current temperature is below the target."""
        return current < self._target


# ---------------- tests (run: pytest task_3_6.py) ----------------
import pytest  # noqa: E402


def test_thermostat_clamps_high_and_low():
    t = Thermostat(10, 30)
    t.target = 100
    assert t.target == 30
    t.target = -5
    assert t.target == 10


def test_thermostat_inside_range_unchanged():
    t = Thermostat(10, 30, target=22)
    assert t.target == 22


def test_thermostat_heating_needed():
    t = Thermostat(10, 30, target=22)
    assert t.heating_needed(20) is True
    assert t.heating_needed(22) is False  # edge: equal
    assert t.heating_needed(25) is False


def test_thermostat_invalid_range():
    with pytest.raises(ValueError):
        Thermostat(30, 10)
