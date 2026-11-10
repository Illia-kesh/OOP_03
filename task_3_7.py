"""Task 3.7 - Inventory (chapter 3: protecting object state)."""

class Inventory:
    """Warehouse: the internal dict is never exposed directly."""

    def __init__(self):
        """Create an empty inventory."""
        self._stock = {}  # item name -> quantity

    @staticmethod
    def _check(name, qty):
        """Validate item name and quantity."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Item name must be a non-empty string")
        if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
            raise ValueError("Quantity must be a positive integer")

    def add(self, name, qty):
        """Add qty units of an item."""
        self._check(name, qty)
        self._stock[name] = self._stock.get(name, 0) + qty

    def remove(self, name, qty):
        """Remove qty units; cannot remove more than available."""
        self._check(name, qty)
        have = self._stock.get(name, 0)
        if qty > have:
            raise ValueError(f"Not enough '{name}': have {have}, requested {qty}")
        if qty == have:
            del self._stock[name]  # do not keep zero-quantity entries
        else:
            self._stock[name] = have - qty

    def quantity(self, name):
        """Return the quantity of an item (0 if it is absent)."""
        return self._stock.get(name, 0)

    def items(self):
        """Return a COPY of the stock dictionary."""
        return dict(self._stock)


# ---------------- tests (run: pytest task_3_7.py) ----------------
import pytest  # noqa: E402


def test_inventory_add_and_quantity():
    inv = Inventory()
    inv.add("apple", 5)
    inv.add("apple", 3)
    assert inv.quantity("apple") == 8
    assert inv.quantity("pear") == 0  # absent item


def test_inventory_remove():
    inv = Inventory()
    inv.add("apple", 5)
    inv.remove("apple", 2)
    assert inv.quantity("apple") == 3
    inv.remove("apple", 3)  # edge: remove everything
    assert inv.items() == {}


def test_inventory_remove_too_much():
    inv = Inventory()
    inv.add("apple", 1)
    with pytest.raises(ValueError):
        inv.remove("apple", 2)
    with pytest.raises(ValueError):
        inv.remove("ghost", 1)


def test_inventory_items_is_copy():
    inv = Inventory()
    inv.add("apple", 1)
    inv.items()["apple"] = 999
    assert inv.quantity("apple") == 1


@pytest.mark.parametrize("qty", [0, -1, 1.5])
def test_inventory_invalid_qty(qty):
    with pytest.raises(ValueError):
        Inventory().add("apple", qty)
