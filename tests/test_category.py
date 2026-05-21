from typing import List

import pytest

from src.category import Category
from src.product import Product


class MockProduct(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int = 0) -> None:
        super().__init__(name, description, price, quantity)

    def __str__(self) -> str:
        return f"{self.name}, {int(self.price)} руб. Остаток: {self.quantity} шт."


@pytest.fixture
def category_data() -> Category:
    p1 = MockProduct("Samsung Galaxy", "Базовый Самсунг", 100000.0, 5)
    p2 = MockProduct("Iphone 15", "Базовый Айфон", 150000.0, 3)
    return Category("Смартфоны", "Современные гаджеты", [p1, p2])


def test_init(category_data: Category) -> None:
    assert category_data.name == "Смартфоны"
    assert Category.category_count >= 1
    assert Category.product_count >= 2


def test_add_product(category_data: Category) -> None:
    current_count = Category.product_count
    new_p = MockProduct("Xiaomi", "Бюджетный хит", 30000.0, 10)
    category_data.add_product(new_p)

    assert Category.product_count == current_count + 1

    products_list: List[Product] = getattr(category_data, "_Category__products")
    assert new_p in products_list


def test_products_property() -> None:
    prod1 = MockProduct("Samsung Galaxy S23 Ultra", "256GB, Серый", 180000.0, 3)
    prod2 = MockProduct("Iphone 15 Pro", "128GB, Титан", 140000.0, 5)
    category = Category("Смартфоны", "Гаджеты", [prod1, prod2])

    assert category.products.strip() == (
        "Samsung Galaxy S23 Ultra, 180000 руб. Остаток: 3 шт.\n"
        "Iphone 15 Pro, 140000 руб. Остаток: 5 шт."
    )
