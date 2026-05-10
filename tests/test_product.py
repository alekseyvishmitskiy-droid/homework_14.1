from typing import Any
from unittest.mock import patch

import pytest

from src.product import Product


@pytest.fixture
def product_iphone() -> Product:
    return Product("Iphone 15", "512GB", 150000.0, 5)


def test_product_init(product_iphone: Product) -> None:
    assert product_iphone.name == "Iphone 15"
    assert product_iphone.price == 150000.0
    assert product_iphone.quantity == 5


def test_new_product_creation() -> None:
    data = {"name": "Samsung", "description": "Android", "price": 80000.0, "quantity": 10}
    new_obj = Product.new_product(data)
    assert new_obj.name == "Samsung"
    assert new_obj.quantity == 10


def test_new_product_update_existing(product_iphone: Product) -> None:
    products_list = [product_iphone]
    data = {"name": "Iphone 15", "description": "New", "price": 160000.0, "quantity": 5}

    updated_product = Product.new_product(data, products_list)

    assert updated_product.quantity == 10
    assert updated_product.price == 160000.0


def test_price_setter_invalid(product_iphone: Product) -> None:
    product_iphone.price = -100
    assert product_iphone.price == 150000.0


@patch("builtins.input", return_value="y")
def test_price_setter_lower_confirm(mock_input: Any, product_iphone: Product) -> None:
    product_iphone.price = 140000.0
    assert product_iphone.price == 140000.0


@patch("builtins.input", return_value="n")
def test_price_setter_lower_cancel(mock_input: Any, product_iphone: Product) -> None:
    product_iphone.price = 140000.0
    assert product_iphone.price == 150000.0
