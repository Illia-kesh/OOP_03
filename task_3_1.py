"""Task 3.1 - BankAccount (chapter 3: protecting object state)."""

class BankAccount:
    """Bank account with an owner and a read-only balance."""

    def __init__(self, owner, balance=0):
        """Create an account.

        Args:
            owner: account holder name.
            balance: initial balance (must not be negative).
        """
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._owner = owner
        self._balance = balance
        self._history = []  # list of (operation, amount) tuples

    @property
    def owner(self):
        """Account holder (read-only)."""
        return self._owner

    @property
    def balance(self):
        """Current balance (read-only, no setter on purpose)."""
        return self._balance

    def deposit(self, amount):
        """Add money to the account. Amount must be positive."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        self._history.append(("deposit", amount))

    def withdraw(self, amount):
        """Take money from the account. Balance can never go below 0."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._history.append(("withdraw", amount))

    def history(self):
        """Return a COPY of the operations list, so callers cannot alter it."""
        return self._history.copy()


# ---------------- tests (run: pytest task_3_1.py) ----------------
import pytest  # noqa: E402


def test_account_deposit_withdraw():
    acc = BankAccount("Enotik", 100)
    acc.deposit(50)
    acc.withdraw(30)
    assert acc.balance == 120
    assert acc.history() == [("deposit", 50), ("withdraw", 30)]


def test_account_balance_read_only():
    acc = BankAccount("Enotik")
    with pytest.raises(AttributeError):
        acc.balance = 1000


def test_account_withdraw_below_zero():
    acc = BankAccount("Enotik", 10)
    with pytest.raises(ValueError):
        acc.withdraw(11)
    acc.withdraw(10)  # edge: exactly the whole balance
    assert acc.balance == 0


def test_account_history_is_copy():
    acc = BankAccount("Enotik")
    acc.deposit(5)
    acc.history().append(("hack", 999))
    assert acc.history() == [("deposit", 5)]


def test_account_invalid_amounts():
    acc = BankAccount("Enotik")
    with pytest.raises(ValueError):
        acc.deposit(0)
    with pytest.raises(ValueError):
        acc.deposit(-5)
