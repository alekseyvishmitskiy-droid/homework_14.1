import pytest

from src.category import Category
from src.product import Product


@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product_iphone() -> Product:
    return Product(name="iPhone 15", description="512GB", price=100000.0, quantity=5)


@pytest.fixture
def product_samsung() -> Product:
    return Product(name="Samsung S24", description="256GB", price=90000.0, quantity=10)


def test_category_init(product_iphone: Product, product_samsung: Product) -> None:
    products_list = [product_iphone, product_samsung]
    category = Category(name="Смартфоны", description="Мобильные телефоны", products=products_list)

    assert category.name == "Смартфоны"
    assert category.description == "Мобильные телефоны"
    assert Category.category_count == 1
    assert Category.product_count == 15


def test_add_product(product_iphone: Product, product_samsung: Product) -> None:
    category = Category(name="Смартфоны", description="Телефоны", products=[product_iphone])
    assert Category.product_count == 5

    category.add_product(product_samsung)
    assert Category.product_count == 15


def test_str_magic_method(product_iphone: Product, product_samsung: Product) -> None:
    category = Category(name="Смартфоны", description="Телефоны", products=[product_iphone, product_samsung])

    assert str(category) == "Смартфоны, количество продуктов: 15 шт."


def test_products_property(product_iphone: Product, product_samsung: Product) -> None:
    category = Category(name="Смартфоны", description="Телефоны", products=[product_iphone, product_samsung])

    expected_output = (
        "iPhone 15, 100000 руб. Остаток: 5 шт.\n"
        "Samsung S24, 90000 руб. Остаток: 10 шт.\n"
    )
    assert category.products == expected_output
