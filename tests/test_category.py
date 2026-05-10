import pytest

from src.category import Category


class MockProduct:
    def __init__(self, name: str, price: float, quantity: int) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity


@pytest.fixture
def category_data() -> Category:
    p1 = MockProduct("Samsung Galaxy", 100000.0, 5)
    p2 = MockProduct("Iphone 15", 150000.0, 3)
    return Category("Смартфоны", "Современные гаджеты", [p1, p2])


def test_init(category_data: Category) -> None:
    assert category_data.name == "Смартфоны"
    assert category_data.category_count == 1
    assert category_data.product_count >= 2


def test_add_product(category_data: Category) -> None:
    current_count = Category.product_count
    new_p = MockProduct("Xiaomi", 30000.0, 10)
    category_data.add_product(new_p)

    assert Category.product_count == current_count + 1
    assert "Xiaomi" in category_data.products


def test_products_property(category_data: Category) -> None:
    expected_output = "Samsung Galaxy, 100000.0 руб. Остаток: 5 шт.\n" "Iphone 15, 150000.0 руб. Остаток: 3 шт.\n"
    assert category_data.products == expected_output


def test_private_products(category_data: Category) -> None:
    with pytest.raises(AttributeError):
        print(category_data.__products)
