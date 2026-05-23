from typing import Any, Dict, List

import pytest

from src.category import Category
from src.product import LawnGrass, Product, Smartphone


@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    """Фикстура для автоматического сброса счетчиков категорий перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product_apple() -> Product:
    """Фикстура для создания стандартного товара."""
    return Product("Яблоки", "Свежие урожайные яблоки", 100.0, 10)


@pytest.fixture
def product_banana() -> Product:
    """Фикстура для создания второго товара."""
    return Product("Бананы", "Спелые бананы", 150.0, 5)


@pytest.fixture
def product_iphone() -> Product:
    """Фикстура для создания iPhone как базового продукта."""
    return Product(name="iPhone 15", description="512GB", price=100000.0, quantity=5)


@pytest.fixture
def product_samsung() -> Product:
    """Фикстура для создания Samsung как базового продукта."""
    return Product(name="Samsung S24", description="256GB", price=90000.0, quantity=10)


@pytest.fixture
def smartphone_s23() -> Smartphone:
    """Фикстура для создания объекта класса Smartphone."""
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
    """Фикстура для создания объекта класса LawnGrass."""
    return LawnGrass(
        name="Газонная трава",
        description="Элитная трава для газона",
        price=500.0,
        quantity=20,
        country="Россия",
        germination_period="7 дней",
        color="Зеленый",
    )


def test_product_init(product_apple: Product) -> None:
    """Тест корректной инициализации атрибутов."""
    assert product_apple.name == "Яблоки"
    assert product_apple.description == "Свежие урожайные яблоки"
    assert product_apple.price == 100.0
    assert product_apple.quantity == 10


def test_product_str(product_apple: Product) -> None:
    """Тест строкового представления __str__."""
    assert str(product_apple) == "Яблоки, 100 руб. Остаток: 10 шт."


def test_price_setter_increase(product_apple: Product) -> None:
    """Тест успешного повышения цены."""
    product_apple.price = 120.0
    assert product_apple.price == 120.0


def test_price_setter_invalid(capsys: pytest.CaptureFixture[str], product_apple: Product) -> None:
    """Тест запрета на установку некорректной цены."""
    product_apple.price = -5.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product_apple.price == 100.0


def test_price_setter_decrease_confirm(monkeypatch: pytest.MonkeyPatch, product_apple: Product) -> None:
    """Тест подтверждения снижения цены."""
    monkeypatch.setattr("builtins.input", lambda _: "y")
    product_apple.price = 80.0
    assert product_apple.price == 80.0


def test_price_setter_decrease_reject(monkeypatch: pytest.MonkeyPatch, product_apple: Product) -> None:
    """Тест отмены снижения цены."""
    monkeypatch.setattr("builtins.input", lambda _: "n")
    product_apple.price = 80.0
    assert product_apple.price == 100.0


def test_new_product_creation() -> None:
    """Тест фабричного метода для создания нового товара."""
    data: Dict[str, Any] = {"name": "Груши", "description": "Сладкие груши", "price": 200.0, "quantity": 3}
    new_prod = Product.new_product(data)
    assert new_prod.name == "Груши"
    assert new_prod.price == 200.0
    assert new_prod.quantity == 3


def test_new_product_merge_existing(product_apple: Product) -> None:
    """Тест объединения товара с уже существующим в списке."""
    products_list = [product_apple]
    data: Dict[str, Any] = {"name": "Яблоки", "description": "Другие яблоки", "price": 130.0, "quantity": 5}

    updated_prod = Product.new_product(data, products_list)

    assert updated_prod is product_apple
    assert updated_prod.quantity == 15
    assert updated_prod.price == 130.0


def test_product_add(product_apple: Product, product_banana: Product) -> None:
    """Тест магического метода сложения стоимости для одинаковых классов."""
    result = product_apple + product_banana
    assert result == 1750.0


def test_product_add_type_error(product_apple: Product) -> None:
    """Тест на вызов TypeError при сложении с неверным типом."""
    invalid_data: Any = 100
    with pytest.raises(TypeError):
        _ = product_apple + invalid_data


def test_smartphone_init(smartphone_s23: Smartphone) -> None:
    """Тест уникальных свойств наследника Smartphone."""
    assert smartphone_s23.name == "Samsung Galaxy S23 Ultra"
    assert smartphone_s23.efficiency == 95.5
    assert smartphone_s23.model == "S23 Ultra"
    assert smartphone_s23.memory == 256
    assert smartphone_s23.color == "Серый"


def test_lawn_grass_init(grass_lawn: LawnGrass) -> None:
    """Тест уникальных свойств наследника LawnGrass."""
    assert grass_lawn.name == "Газонная трава"
    assert grass_lawn.country == "Россия"
    assert grass_lawn.germination_period == "7 дней"
    assert grass_lawn.color == "Зеленый"


def test_invalid_addition_different_classes_raises_type_error(
    smartphone_s23: Smartphone, grass_lawn: LawnGrass
) -> None:
    """Тест падения с TypeError при попытке сложить смартфон и траву."""
    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов!"):
        _ = smartphone_s23 + grass_lawn


def test_category_init(product_iphone: Product, product_samsung: Product) -> None:
    """Тест инициализации категории и работы глобальных счетчиков позиций."""
    products_list: List[Product] = [product_iphone, product_samsung]
    category = Category(name="Смартфоны", description="Мобильные телефоны", products=products_list)

    assert category.name == "Смартфоны"
    assert category.description == "Мобильные телефоны"
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_add_product(product_iphone: Product, product_samsung: Product) -> None:
    """Тест метода add_product и обновления счетчика уникальных позиций."""
    category = Category(name="Смартфоны", description="Телефоны", products=[product_iphone])
    assert Category.product_count == 1

    category.add_product(product_samsung)
    assert Category.product_count == 2


def test_category_str_magic_method(product_iphone: Product, product_samsung: Product) -> None:
    """Тест магического метода __str__ для категорий (сумма штук товаров: 5 + 10 = 15)."""
    category = Category(name="Смартфоны", description="Телефоны", products=[product_iphone, product_samsung])
    assert str(category) == "Смартфоны, количество продуктов: 15 шт."


def test_category_products_property(product_iphone: Product, product_samsung: Product) -> None:
    """Тест свойства products, возвращающего список строк."""
    category = Category(name="Смартфоны", description="Телефоны", products=[product_iphone, product_samsung])

    expected_output = [
        "iPhone 15, 100000 руб. Остаток: 5 шт.",
        "Samsung S24, 90000 руб. Остаток: 10 шт.",
    ]
    assert category.products == expected_output


def test_add_invalid_product_to_category_raises_type_error() -> None:
    """Тест защиты add_product от добавления невалидных типов объектов (строк/чисел)."""
    category = Category(name="Смартфоны", description="Телефоны", products=[])

    with pytest.raises(TypeError, match="Можно добавлять только продукты или их наследников!"):
        category.add_product("Not a product")


def test_category_init_with_invalid_product_raises_type_error() -> None:
    """Тест защиты __init__ от передачи некорректных типов данных при создании категории."""
    invalid_list: List[Any] = ["Just a string", 42]

    with pytest.raises(TypeError, match="Можно добавлять только продукты или их наследников!"):
        Category(name="Тест", description="Тест", products=invalid_list)
