"""Task 3.5 - Rectangle (chapter 3: protecting object state)."""

class Rectangle:
    """Rectangle with positive sides and computed area/perimeter."""

    def __init__(self, width, height):
        """Create a rectangle; both sides must be positive."""
        self.width = width
        self.height = height

    @staticmethod
    def _check_side(value, label):
        """Validate that a side is a positive number."""
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"{label} must be a positive number")
        return value

    @property
    def width(self):
        """Width (positive)."""
        return self._width

    @width.setter
    def width(self, value):
        """Set the width; must be positive."""
        self._width = self._check_side(value, "Width")

    @property
    def height(self):
        """Height (positive)."""
        return self._height

    @height.setter
    def height(self, value):
        """Set the height; must be positive."""
        self._height = self._check_side(value, "Height")

    @property
    def area(self):
        """Area (computed, read-only)."""
        return self._width * self._height

    @property
    def perimeter(self):
        """Perimeter (computed, read-only)."""
        return 2 * (self._width + self._height)


# ---------------- tests (run: pytest task_3_5.py) ----------------
import pytest  # noqa: E402


def test_rectangle_area_perimeter():
    r = Rectangle(3, 4)
    assert r.area == 12
    assert r.perimeter == 14


def test_rectangle_update_side():
    r = Rectangle(3, 4)
    r.width = 5
    assert r.area == 20


@pytest.mark.parametrize("bad", [0, -1, "5", None])
def test_rectangle_invalid_side(bad):
    with pytest.raises(ValueError):
        Rectangle(bad, 2)
    with pytest.raises(ValueError):
        Rectangle(2, bad)


def test_rectangle_area_read_only():
    with pytest.raises(AttributeError):
        Rectangle(1, 1).area = 5
