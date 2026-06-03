import json
from collections.abc import Generator
from pathlib import Path
from typing import Any, List
from unittest.mock import patch

import pytest

from src.category import Category, Order
from src.product import LawnGrass, Product, Smartphone
from src.utils import read_json


@pytest.fixture(autouse=True)
def reset_category_counters() -> Generator[None, None, None]:
    """Сбрасывает счетчики до и после каждого теста для изоляции."""
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture(autouse=True)
def mock_input() -> Generator[None, None, None]:
    """Автоматически подменяет input(), чтобы тесты не зависали."""
    with patch("builtins.input", return_value="y"):
        yield


@pytest.fixture
def product_iphone() -> Product:
    return Product(name="iPhone 15", description="512GB", price=100000.0, quantity=5)


@pytest.fixture
def product_samsung() -> Product:
    return Product(name="Samsung S24", description="256GB", price=90000.0, quantity=10)


@pytest.fixture
def smartphone_s23() -> Smartphone:
    return Smartphone(
        name="Samsung Galaxy S23 Ultra",
        description="256GB, Серый цвет",
        price=180000.0,
        quantity=5,
        efficiency=95.5,
        model="S23 Ultra",
        memory=256,
        color="Серый",
    )


@pytest.fixture
def grass_lawn() -> LawnGrass:
    return LawnGrass(
        name="Газонная трава",
        description="Элитная трава для газона",
        price=500.0,
        quantity=20,
        country="Россия",
        germination_period="7 дней",
        color="Зеленый",
    )


def test_category_init(product_iphone: Product, product_samsung: Product) -> None:
    products_list = [product_iphone, product_samsung]
    category = Category(name="Смартфоны", description="Мобильные телефоны", products=products_list)

    assert category.name == "Смартфоны"
    assert category.description == "Мобильные телефоны"
    assert Category.category_count == 1
    assert Category.product_count == 2
    assert category.total_quantity == 15
    assert category.total_cost == 1400000.0


def test_add_product(product_iphone: Product, product_samsung: Product) -> None:
    category = Category(name="Смартфоны", description="Телефоны", products=[product_iphone])
    assert Category.product_count == 1

    category.add_product(product_samsung)
    assert Category.product_count == 2


def test_str_magic_method(product_iphone: Product, product_samsung: Product) -> None:
    category = Category(name="Смартфоны", description="Телефоны", products=[product_iphone, product_samsung])

    assert str(category) == "Смартфоны, количество продуктов: 15 шт."


def test_products_property(product_iphone: Product, product_samsung: Product) -> None:
    """Тест свойства products, возвращающего список строк с целочисленными ценами."""
    category = Category(name="Смартфоны", description="Телефоны", products=[product_iphone, product_samsung])

    expected_output = [
        "iPhone 15, 100000 руб. Остаток: 5 шт.",
        "Samsung S24, 90000 руб. Остаток: 10 шт.",
    ]
    assert category.products == expected_output


def test_smartphone_init(smartphone_s23: Smartphone) -> None:
    assert smartphone_s23.name == "Samsung Galaxy S23 Ultra"
    assert smartphone_s23.efficiency == 95.5
    assert smartphone_s23.model == "S23 Ultra"
    assert smartphone_s23.memory == 256
    assert smartphone_s23.color == "Серый"


def test_lawn_grass_init(grass_lawn: LawnGrass) -> None:
    assert grass_lawn.name == "Газонная трава"
    assert grass_lawn.country == "Россия"
    assert grass_lawn.germination_period == "7 дней"
    assert grass_lawn.color == "Зеленый"


def test_valid_addition(smartphone_s23: Smartphone) -> None:
    smartphone_another = Smartphone(
        name="Iphone 15",
        description="512GB",
        price=210000.0,
        quantity=8,
        efficiency=98.2,
        model="15",
        memory=512,
        color="Space Gray",
    )
    assert smartphone_s23 + smartphone_another == 2580000.0


def test_invalid_addition_raises_type_error(smartphone_s23: Smartphone, grass_lawn: LawnGrass) -> None:
    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов!"):
        _ = smartphone_s23 + grass_lawn


def test_add_invalid_product_to_category_raises_type_error() -> None:
    category = Category(name="Смартфоны", description="Телефоны", products=[])

    with pytest.raises(TypeError, match="Можно добавлять только продукты или их наследников!"):
        category.add_product("Not a product")  # type: ignore[arg-type]


def test_category_init_with_invalid_product_raises_type_error() -> None:
    invalid_list: List[Any] = ["Just a string", 123]

    with pytest.raises(TypeError, match="Можно добавлять только продукты или их наследников!"):
        Category(name="Гнилой товар", description="Тест", products=invalid_list)

    # Проверка, что из-за падения счетчик категорий не увеличился
    assert Category.category_count == 0


def test_order_init_success(product_iphone: Product) -> None:
    order = Order(product=product_iphone, quantity=3)

    assert order.product == product_iphone
    assert order.total_quantity == 3
    assert order.total_cost == 300000.0
    assert str(order) == "Заказ: iPhone 15 x 3 шт. Итоговая стоимость: 300000 руб."


def test_order_init_raises_type_error() -> None:
    with pytest.raises(TypeError, match="В заказ можно добавить только продукт или его наследника!"):
        Order(product="Not a product", quantity=5)  # type: ignore[arg-type]


def test_read_json_success(tmp_path: Path) -> None:
    data = [
        {
            "name": "Смартфоны",
            "description": "Тест",
            "products": [{"name": "Iphone", "description": "X", "price": 1000.0, "quantity": 1}],
        }
    ]

    p = tmp_path / "products.json"
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    result: List[Category] = read_json(str(p))

    assert len(result) == 1
    assert isinstance(result[0], Category)
    assert result[0].name == "Смартфоны"
    assert result[0].description == "Тест"

    assert len(result[0].products) == 1
    product_str = result[0].products[0]

    assert isinstance(product_str, str)
    assert "Iphone" in product_str


def test_read_json_empty(tmp_path: Path) -> None:
    p = tmp_path / "empty.json"
    p.write_text(json.dumps([]), encoding="utf-8")

    result: List[Category] = read_json(str(p))
    assert result == []


def test_read_json_no_products_key(tmp_path: Path) -> None:
    data = [{"name": "Пустая категория", "description": "Без продуктов"}]

    p = tmp_path / "no_products.json"
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    result: List[Category] = read_json(str(p))

    assert len(result) == 1
    assert result[0].products == []
