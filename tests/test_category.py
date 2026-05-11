import pytest
from src.category import Category

class MockProduct:
    def __init__(self, name: str, price: float, quantity: int) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity

@pytest.fixture(autouse=True)
def reset_counters():
    Category.category_count = 0
    Category.product_count = 0

@pytest.fixture
def category_data() -> Category:
    p1 = MockProduct("Samsung Galaxy", 100000, 5)
    p2 = MockProduct("Iphone 15", 150000, 3)
    return Category("Смартфоны", "Современные гаджеты", [p1, p2])

def test_init(category_data: Category) -> None:
    assert category_data.name == "Смартфоны"
    assert category_data.description == "Современные гаджеты"
    assert Category.category_count == 1
    assert Category.product_count == 2

def test_add_product(category_data: Category) -> None:
    initial_count = Category.product_count
    new_p = MockProduct("Xiaomi", 30000, 10)
    category_data.add_product(new_p)

    assert Category.product_count == initial_count + 1
    assert new_p in category_data._Category__products

def test_products_property(category_data: Category) -> None:
    expected_output = (
        "Samsung Galaxy, 100000 руб. Остаток: 5 шт.\n"
        "Iphone 15, 150000 руб. Остаток: 3 шт.\n"
    )
    assert category_data.products == expected_output

def test_private_products_access(category_data: Category) -> None:
    with pytest.raises(AttributeError):
        _ = category_data.__products
