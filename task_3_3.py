"""Task 3.3 - Person (chapter 3: protecting object state)."""

class Person:
    """Person with a validated name and age."""

    def __init__(self, name, age):
        """Create a person; name and age are validated by the setters."""
        self.name = name
        self.age = age

    @property
    def name(self):
        """Name (non-empty, stripped)."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the name: must be a non-empty string; edge spaces are removed."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()

    @property
    def age(self):
        """Age in years (0..150)."""
        return self._age

    @age.setter
    def age(self, value):
        """Set the age: integer in range 0..150."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("Age must be an integer")
        if not 0 <= value <= 150:
            raise ValueError("Age must be between 0 and 150")
        self._age = value

    @property
    def is_adult(self):
        """True if the person is 18 or older (read-only)."""
        return self._age >= 18


# ---------------- tests (run: pytest task_3_3.py) ----------------
import pytest  # noqa: E402


def test_person_name_stripped():
    assert Person("  Anna  ", 20).name == "Anna"


def test_person_is_adult():
    assert Person("A", 18).is_adult is True
    assert Person("A", 17).is_adult is False


def test_person_is_adult_read_only():
    p = Person("A", 20)
    with pytest.raises(AttributeError):
        p.is_adult = False


@pytest.mark.parametrize("bad_age", [-1, 151, "20", 3.5])
def test_person_invalid_age(bad_age):
    with pytest.raises(ValueError):
        Person("A", bad_age)


@pytest.mark.parametrize("bad_name", ["", "   ", None])
def test_person_invalid_name(bad_name):
    with pytest.raises(ValueError):
        Person(bad_name, 20)


def test_person_age_bounds():
    assert Person("A", 0).age == 0
    assert Person("A", 150).age == 150
