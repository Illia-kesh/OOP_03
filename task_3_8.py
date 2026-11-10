"""Task 3.8 - Student (chapter 3: protecting object state)."""

class Student:
    """Student with an immutable id, validated name and protected grades."""

    def __init__(self, student_id, name):
        """Create a student; the id can never change afterwards."""
        self._id = student_id
        self.name = name
        self._grades = []

    @property
    def id(self):
        """Student id (read-only)."""
        return self._id

    @property
    def name(self):
        """Student name (non-empty, stripped)."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the name; must be a non-empty string."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()

    @property
    def grades(self):
        """Grades as a tuple, so they cannot be modified from outside."""
        return tuple(self._grades)

    def add_grade(self, grade):
        """Add a grade (a number from 0 to 100)."""
        if isinstance(grade, bool) or not isinstance(grade, (int, float)):
            raise ValueError("Grade must be a number")
        if not 0 <= grade <= 100:
            raise ValueError("Grade must be between 0 and 100")
        self._grades.append(grade)


# ---------------- tests (run: pytest task_3_8.py) ----------------
import pytest  # noqa: E402


def test_student_id_read_only():
    s = Student(1, "Ivan")
    with pytest.raises(AttributeError):
        s.id = 2


def test_student_grades_tuple_immutable():
    s = Student(1, "Ivan")
    s.add_grade(90)
    assert s.grades == (90,)
    assert isinstance(s.grades, tuple)
    with pytest.raises(AttributeError):
        s.grades.append(100)
    with pytest.raises(AttributeError):
        s.grades = (1, 2)


@pytest.mark.parametrize("bad", [-1, 101, "A"])
def test_student_invalid_grade(bad):
    with pytest.raises(ValueError):
        Student(1, "Ivan").add_grade(bad)


def test_student_name_validation():
    s = Student(1, "  Ivan ")
    assert s.name == "Ivan"
    with pytest.raises(ValueError):
        s.name = "  "
