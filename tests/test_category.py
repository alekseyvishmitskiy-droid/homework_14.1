import pytest
from src.category import Category
from src.product import Product


@pytest.fixture
def products_list():
    return [
        Product("Iphone", "iOS", 1000.0, 2),
        Product("Xiaomi", "Android", 500.0, 10)
    ]


def test_category_init(products_list):
    Category.category_count = 0
    Category.product_count = 0

    category = Category("Smartphones", "Modern phones", products_list)

    assert category.name == "Smartphones"
    assert len(category.products) == 2
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_multiple_categories(products_list):
    Category.category_count = 0
    Category.product_count = 0

    cat1 = Category("Electronics", "Desc", products_list)
    cat2 = Category("Gadgets", "Desc", [products_list[0]])

    assert Category.category_count == 2
    assert Category.product_count == 3


