from typing import Any

import pytest

from src.product import Product


@pytest.fixture
def product_apple() -> Product:
    return Product("Яблоки", "Свежие урожайные яблоки", 100.0, 10)


@pytest.fixture
def product_banana() -> Product:
    return Product("Бананы", "Спелые бананы", 150.0, 5)


def test_product_init(product_apple: Product) -> None:
    assert product_apple.name == "Яблоки"
    assert product_apple.description == "Свежие урожайные яблоки"
    assert product_apple.price == 100.0
    assert product_apple.quantity == 10


def test_product_str(product_apple: Product) -> None:
    assert str(product_apple) == "Яблоки, 100 руб. Остаток: 10 шт."


def test_price_setter_increase(product_apple: Product) -> None:
    product_apple.price = 120.0
    assert product_apple.price == 120.0


def test_price_setter_invalid(capsys: pytest.CaptureFixture[str], product_apple: Product) -> None:
    product_apple.price = -5.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product_apple.price == 100.0


def test_price_setter_decrease_confirm(monkeypatch: pytest.MonkeyPatch, product_apple: Product) -> None:
    monkeypatch.setattr('builtins.input', lambda _: "y")
    product_apple.price = 80.0
    assert product_apple.price == 80.0


def test_price_setter_decrease_reject(monkeypatch: pytest.MonkeyPatch, product_apple: Product) -> None:
    monkeypatch.setattr('builtins.input', lambda _: "n")
    product_apple.price = 80.0
    assert product_apple.price == 100.0


def test_new_product_creation() -> None:
    data = {
        "name": "Груши",
        "description": "Сладкие груши",
        "price": 200.0,
        "quantity": 3
    }
    new_prod = Product.new_product(data)
    assert new_prod.name == "Груши"
    assert new_prod.price == 200.0
    assert new_prod.quantity == 3


def test_new_product_merge_existing(product_apple: Product) -> None:
    products_list = [product_apple]
    data = {
        "name": "Яблоки",
        "description": "Другие яблоки",
        "price": 130.0,
        "quantity": 5
    }

    updated_prod = Product.new_product(data, products_list)

    assert updated_prod is product_apple
    assert updated_prod.quantity == 15
    assert updated_prod.price == 130.0


def test_product_add(product_apple: Product, product_banana: Product) -> None:
    result = product_apple + product_banana
    assert result == 1750.0


def test_product_add_type_error(product_apple: Product) -> None:
    invalid_data: Any = 100
    with pytest.raises(TypeError) as exc_info:
        product_apple.__add__(invalid_data)
    assert str(exc_info.value) == "Складывать можно только объекты класса Product"
