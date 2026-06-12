from collections.abc import Generator

import pytest

from src.category import Category, Order
from src.product import LawnGrass, Smartphone


@pytest.fixture(autouse=True)
def reset_category_counters() -> Generator[None, None, None]:
    """Фикстура для сброса счетчиков класса Category перед каждым тестом.

    Сбрасывает только реально существующие статические атрибуты класса.
    """
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def sample_smartphone() -> Smartphone:
    """Фикстура смартфона для тестов категорий и заказов."""
    return Smartphone(
        name="iPhone 15",
        description="Флагман",
        price=120000.0,
        quantity=5,
        efficiency=4.5,
        model="Pro",
        memory=256,
        color="Titanium",
    )


@pytest.fixture
def sample_grass() -> LawnGrass:
    """Фикстура газонной травы для тестов категорий и заказов."""
    return LawnGrass(
        name="Изумруд",
        description="Густая трава",
        price=500.0,
        quantity=20,
        country="Россия",
        germination_period="14 дней",
        color="Зеленый",
    )


def test_category_init(sample_smartphone: Smartphone, sample_grass: LawnGrass) -> None:
    """Тест инициализации категории и корректного подсчета счетчиков."""
    products = [sample_smartphone, sample_grass]
    category = Category("Электроника и Сад", "Разные товары", products)

    assert category.name == "Электроника и Сад"
    assert Category.category_count == 1
    assert Category.product_count == 2
    assert category.total_quantity == 25  # 5 + 20
    assert category.total_cost == (120000.0 * 5) + (500.0 * 20)


def test_category_add_product_counting(sample_smartphone: Smartphone) -> None:
    """Тест добавления товаров и увеличения общего счетчика количества продуктов."""
    category = Category("Смартфоны", "Гаджеты", [sample_smartphone])
    assert Category.product_count == 1

    duplicate_phone = Smartphone(
        name="iPhone 15",
        description="Другой цвет",
        price=120000.0,
        quantity=2,
        efficiency=4.5,
        model="Pro",
        memory=256,
        color="Black",
    )
    category.add_product(duplicate_phone)

    assert Category.product_count == 2
    assert category.total_quantity == 7


def test_category_invalid_product_type() -> None:
    """Тест вызова TypeError при передаче некорректного типа в категорию."""
    with pytest.raises(TypeError, match="Можно добавлять только продукты или их наследников!"):
        Category("Тест", "Описание", ["Строка вместо продукта"])


def test_category_products_string_list(sample_smartphone: Smartphone) -> None:
    """Тест свойства products, которое должно возвращать список строковых представлений."""
    category = Category("Смартфоны", "Гаджеты", [sample_smartphone])
    assert category.products == ["iPhone 15, 120000 руб. Остаток: 5 шт."]


def test_category_string_representation(sample_smartphone: Smartphone) -> None:
    """Тест строкового представления категории (__str__)."""
    category = Category("Смартфоны", "Гаджеты", [sample_smartphone])
    assert str(category) == "Смартфоны, количество продуктов: 5 шт."


def test_order_creation_success(sample_smartphone: Smartphone) -> None:
    """Тест успешного оформления заказа и расчета стоимости."""
    order = Order(product=sample_smartphone, quantity=3)

    assert order.product == sample_smartphone
    assert order.total_quantity == 3
    assert order.total_cost == 120000.0 * 3


def test_order_invalid_product_type() -> None:
    """Тест вызова TypeError при передаче не-Product объекта в Order."""
    with pytest.raises(TypeError, match="В заказ можно добавить только продукт или его наследника!"):
        Order(product="Не продукт", quantity=1)  # type: ignore[arg-type]


def test_order_string_representation(sample_smartphone: Smartphone) -> None:
    """Тест строкового представления заказа (__str__)."""
    order = Order(product=sample_smartphone, quantity=2)
    assert str(order) == "Заказ: iPhone 15 x 2 шт. Итоговая стоимость: 240000 руб."
