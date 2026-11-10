"""Task 3.4 - Password (chapter 3: protecting object state)."""

import hashlib
import hmac
import os


class Password:
    """Stores only a salted hash of the password, never the password itself."""

    MIN_LENGTH = 8
    _ITERATIONS = 100_000

    def __init__(self, password):
        """Create the object with an initial password."""
        self.set(password)

    @staticmethod
    def _hash(password, salt):
        """Derive a hash from the password and salt (PBKDF2-HMAC-SHA256)."""
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, Password._ITERATIONS
        )

    def set(self, new):
        """Replace the password. It must be at least 8 characters long."""
        if not isinstance(new, str) or len(new) < self.MIN_LENGTH:
            raise ValueError(f"Password must be at least {self.MIN_LENGTH} characters")
        self._salt = os.urandom(16)  # fresh random salt for every password
        self._hash_value = self._hash(new, self._salt)

    def check(self, candidate):
        """Return True if candidate matches the stored password."""
        if not isinstance(candidate, str):
            return False
        # compare_digest avoids timing attacks
        return hmac.compare_digest(self._hash_value, self._hash(candidate, self._salt))


# ---------------- tests (run: pytest task_3_4.py) ----------------
import pytest  # noqa: E402


def test_password_check_correct_and_wrong():
    p = Password("secret123")
    assert p.check("secret123") is True
    assert p.check("wrong-pass") is False


def test_password_not_stored_in_plain_text():
    p = Password("secret123")
    assert "secret123" not in str(vars(p))
    assert not hasattr(p, "password")


def test_password_too_short():
    with pytest.raises(ValueError):
        Password("short")
    p = Password("12345678")  # edge: exactly 8 characters
    with pytest.raises(ValueError):
        p.set("1234567")


def test_password_change():
    p = Password("oldpassword")
    p.set("newpassword")
    assert p.check("newpassword")
    assert not p.check("oldpassword")
