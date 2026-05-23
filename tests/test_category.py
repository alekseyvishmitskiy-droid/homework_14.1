import json
from pathlib import Path
from typing import Any, List
from unittest.mock import patch

import pytest

from src.category import Category
from src.product import LawnGrass, Product, Smartphone
from src.utils import read_json


@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture(autouse=True)
def mock_input() -> Any:
    """Автоматически подменяет input(), возвращая 'y', чтобы тесты не зависали."""
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


def test_add_product(product_iphone: Product, product_samsung: Product) -> None:
    category = Category(name="Смартфоны", description="Телефоны", products=[product_iphone])
    assert Category.product_count == 1

    category.add_product(product_samsung)
    assert Category.product_count == 2


def test_str_magic_method(product_iphone: Product, product_samsung: Product) -> None:
    category = Category(name="Смартфоны", description="Телефоны", products=[product_iphone, product_samsung])

    assert str(category) == "Смартфоны, количество продуктов: 15 шт."


def test_products_property(product_iphone: Product, product_samsung: Product) -> None:
    category = Category(name="Смартфоны", description="Телефоны", products=[product_iphone, product_samsung])

    expected_output = [
        "iPhone 15, 100000 руб. Остаток: 5 шт.",
        "Samsung S24, 90000 руб. Остаток: 10 шт.",
    ]
    assert category.products == expected_output


def test_smartphone_init(smartphone_s23: Smartphone) -> None:
    """Проверка корректности инициализации уникальных свойств Smartphone."""
    assert smartphone_s23.name == "Samsung Galaxy S23 Ultra"
    assert smartphone_s23.efficiency == 95.5
    assert smartphone_s23.model == "S23 Ultra"
    assert smartphone_s23.memory == 256
    assert smartphone_s23.color == "Серый"


def test_lawn_grass_init(grass_lawn: LawnGrass) -> None:
    """Проверка корректности инициализации уникальных свойств LawnGrass."""
    assert grass_lawn.name == "Газонная трава"
    assert grass_lawn.country == "Россия"
    assert grass_lawn.germination_period == "7 дней"
    assert grass_lawn.color == "Зеленый"


def test_valid_addition(smartphone_s23: Smartphone) -> None:
    """Проверка сложения стоимости товаров одного и того же класса."""
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
    """Проверка возбуждения TypeError при сложении разных классов."""
    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов!"):
        _ = smartphone_s23 + grass_lawn


def test_add_invalid_product_to_category_raises_type_error() -> None:
    """Проверка защиты add_product от добавления объектов, не являющихся Product/наследниками."""
    category = Category(name="Смартфоны", description="Телефоны", products=[])

    with pytest.raises(TypeError, match="Можно добавлять только продукты или их наследников!"):
        category.add_product("Not a product")


def test_category_init_with_invalid_product_raises_type_error() -> None:
    """Проверка защиты конструктора __init__ от добавления некорректных типов при создании."""
    invalid_list: List[Any] = ["Just a string", 123]

    with pytest.raises(TypeError, match="Можно добавлять только продукты или их наследников!"):
        Category(name="Гнилой товар", description="Тест", products=invalid_list)


def test_read_json_success(tmp_path: Path) -> None:
    """Тест успешного парсинга JSON и наполнения категории."""
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
    assert "1000" in product_str


def test_read_json_empty(tmp_path: Path) -> None:
    """Тест чтения пустого списка категорий."""
    p = tmp_path / "empty.json"
    p.write_text(json.dumps([]), encoding="utf-8")

    result: List[Category] = read_json(str(p))
    assert result == []


def test_read_json_no_products_key(tmp_path: Path) -> None:
    """Тест на случай отсутствия ключа 'products' у категории в JSON."""
    data = [{"name": "Пустая категория", "description": "Без продуктов"}]

    p = tmp_path / "no_products.json"
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    result: List[Category] = read_json(str(p))

    assert len(result) == 1
    assert result[0].products == []
