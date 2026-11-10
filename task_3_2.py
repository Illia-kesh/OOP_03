"""Task 3.2 - Temperature (chapter 3: protecting object state)."""

class Temperature:
    """Temperature stored in Celsius with a computed Fahrenheit view."""

    ABSOLUTE_ZERO_C = -273.15

    def __init__(self, celsius=0.0):
        """Create a temperature in degrees Celsius."""
        self.celsius = celsius  # goes through the validating setter

    @property
    def celsius(self):
        """Temperature in Celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """Set Celsius; values below absolute zero are rejected."""
        if value < self.ABSOLUTE_ZERO_C:
            raise ValueError("Temperature cannot be below -273.15 C")
        self._celsius = float(value)

    @property
    def fahrenheit(self):
        """Temperature in Fahrenheit (computed from Celsius)."""
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        """Set Fahrenheit; converts and reuses the Celsius validation."""
        self.celsius = (value - 32) * 5 / 9


# ---------------- tests (run: pytest task_3_2.py) ----------------
import pytest  # noqa: E402


def test_temperature_conversion():
    t = Temperature(100)
    assert t.fahrenheit == pytest.approx(212)


def test_temperature_set_fahrenheit():
    t = Temperature()
    t.fahrenheit = 32
    assert t.celsius == pytest.approx(0)


def test_temperature_absolute_zero_edge():
    t = Temperature(-273.15)  # edge: allowed
    assert t.celsius == -273.15


def test_temperature_below_absolute_zero():
    t = Temperature()
    with pytest.raises(ValueError):
        t.celsius = -273.16
    with pytest.raises(ValueError):
        t.fahrenheit = -500  # also rejected via fahrenheit
