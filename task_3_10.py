"""Task 3.10 - Email (chapter 3: protecting object state)."""

class Email:
    """Email address with validation; user and domain are read-only."""

    def __init__(self, address):
        """Create an email object; the address is validated."""
        self.address = address

    @property
    def address(self):
        """Full address."""
        return self._address

    @address.setter
    def address(self, value):
        """Set the address: exactly one '@', non-empty parts, dot in domain."""
        if not isinstance(value, str) or value.count("@") != 1:
            raise ValueError("Address must contain exactly one '@'")
        user, domain = value.split("@")
        if not user or not domain:
            raise ValueError("User and domain must not be empty")
        # the dot must not be the first or last character of the domain
        if "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise ValueError("Domain must contain a dot inside it")
        self._address = value

    @property
    def user(self):
        """Part before '@' (read-only)."""
        return self._address.split("@")[0]

    @property
    def domain(self):
        """Part after '@' (read-only)."""
        return self._address.split("@")[1]


# ---------------- tests (run: pytest task_3_10.py) ----------------
import pytest  # noqa: E402


def test_email_valid_parts():
    e = Email("user@example.com")
    assert e.user == "user"
    assert e.domain == "example.com"


def test_email_user_domain_read_only():
    e = Email("user@example.com")
    with pytest.raises(AttributeError):
        e.user = "x"
    with pytest.raises(AttributeError):
        e.domain = "x.org"


@pytest.mark.parametrize("bad", [
    "no-at-sign.com", "a@@b.com", "a@b@c.com", "@example.com",
    "user@", "user@localhost", "user@.com", "user@com.", "",
])
def test_email_invalid(bad):
    with pytest.raises(ValueError):
        Email(bad)


def test_email_setter_validates():
    e = Email("a@b.com")
    with pytest.raises(ValueError):
        e.address = "broken"
    assert e.address == "a@b.com"  # old value is kept
