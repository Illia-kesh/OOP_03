"""Task 3.9 - Circle (chapter 3: protecting object state)."""

import math


class Circle:
    """Circle with a lazily computed, cached area."""

    def __init__(self, radius):
        """Create a circle with a positive radius."""
        self._area = None          # cache; None means "needs recomputing"
        self._compute_count = 0    # how many times the area was calculated
        self.radius = radius

    @property
    def radius(self):
        """Radius (positive)."""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Set the radius and invalidate the cached area."""
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Radius must be a positive number")
        self._radius = value
        self._area = None  # radius changed -> cache is stale

    @property
    def area(self):
        """Area; recomputed only when the radius has changed."""
        if self._area is None:
            self._area = math.pi * self._radius ** 2
            self._compute_count += 1
        return self._area

    @property
    def compute_count(self):
        """Number of real area calculations (used to verify the cache)."""
        return self._compute_count


# ---------------- tests (run: pytest task_3_9.py) ----------------
import pytest  # noqa: E402


def test_circle_area_value():
    import math
    assert Circle(2).area == pytest.approx(math.pi * 4)


def test_circle_cache_used():
    c = Circle(1)
    c.area
    c.area
    c.area
    assert c.compute_count == 1  # computed only once


def test_circle_cache_invalidated_on_change():
    c = Circle(1)
    c.area
    c.radius = 2
    c.area
    c.area
    assert c.compute_count == 2


@pytest.mark.parametrize("bad", [0, -3, "1"])
def test_circle_invalid_radius(bad):
    with pytest.raises(ValueError):
        Circle(bad)
