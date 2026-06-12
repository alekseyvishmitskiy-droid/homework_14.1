from typing import Any, Dict, List
from unittest.mock import patch

import pytest

from src.product import BaseProduct, LawnGrass, Product, Smartphone


@pytest.fixture
def product_data() -> Dict[str, Any]:
    """Словарь данных для фабричного метода."""
    return {"name": "iPhone 15", "description": "512GB", "price": 100000.0, "quantity": 5}


@pytest.fixture
def product_iphone() -> Product:
    """Фикстура базового продукта."""
    return Product(name="iPhone 15", description="512GB", price=100000.0, quantity=5)


@pytest.fixture
def smartphone_s23() -> Smartphone:
    """Фикстура смартфона (наследник Product)."""
    return Smartphone(
        name="Samsung Galaxy S23 Ultra",
        description="256GB",
        price=180000.0,
        quantity=5,
        efficiency=95.5,
        model="S23 Ultra",
        memory=256,
        color="Серый",
    )


def test_base_product_instantiation_error() -> None:
    """Проверка, что абстрактный класс BaseProduct нельзя инициализировать."""
    with pytest.raises(TypeError):
        _ = BaseProduct("Тест", "Описание", 10.0, 1) # type: ignore[abstract]


def test_log_mixin_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    """Проверка, что LogMixin выводит лог создания объекта в консоль."""
    _ = Product(name="Тест Лога", description="Миксин", price=500.0, quantity=2)
    captured = capsys.readouterr()
    assert "Был создан объект: Product" in captured.out
    assert "Тест Лога" in captured.out


def test_product_zero_quantity_raises_value_error() -> None:
    """Тест запрета создания товара с нулевым количеством (из BaseProduct)."""
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Ноль", "Описание", 100.0, 0)


def test_product_str(product_iphone: Product) -> None:
    """Проверка строкового отображения продукта."""
    assert str(product_iphone) == "iPhone 15, 100000 руб. Остаток: 5 шт."


def test_price_setter_increase(product_iphone: Product) -> None:
    """Проверка успешного повышения цены."""
    product_iphone.price = 120000.0
    assert product_iphone.price == 120000.0


def test_price_setter_invalid(product_iphone: Product, capsys: pytest.CaptureFixture[str]) -> None:
    """Проверка запрета на установку нулевой или отрицательной цены."""
    product_iphone.price = -100.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product_iphone.price == 100000.0


def test_price_setter_decrease_confirmed(product_iphone: Product) -> None:
    """Проверка снижения цены при подтверждении пользователем ('y')."""
    with patch("builtins.input", return_value="y"):
        product_iphone.price = 90000.0
    assert product_iphone.price == 90000.0


def test_price_setter_decrease_rejected(product_iphone: Product) -> None:
    """Проверка отмены снижения цены при отказе пользователя ('n')."""
    with patch("builtins.input", return_value="n"):
        product_iphone.price = 90000.0
    assert product_iphone.price == 100000.0


def test_new_product_creation(product_data: Dict[str, Any]) -> None:
    """Проверка создания совершенно нового продукта через фабричный метод."""
    product = Product.new_product(product_data)
    assert product.name == "iPhone 15"
    assert product.quantity == 5
    assert product.price == 100000.0


def test_new_product_existing_merge(product_data: Dict[str, Any], product_iphone: Product) -> None:
    """Проверка объединения количества и выбора максимальной цены для дубликата."""
    products_list: List[Product] = [product_iphone]

    product_data["price"] = 110000.0
    product_data["quantity"] = 3

    merged_product = Product.new_product(product_data, products_list)

    assert merged_product is product_iphone
    assert merged_product.quantity == 8
    assert merged_product.price == 110000.0


def test_add_same_classes(smartphone_s23: Smartphone) -> None:
    """Проверка сложения продуктов одного и того же дочернего класса."""
    smartphone_2 = Smartphone(
        name="Samsung Galaxy S23 Ultra",
        description="Второй",
        price=150000.0,
        quantity=2,
        efficiency=95.5,
        model="S23 Ultra",
        memory=256,
        color="Черный",
    )
    assert smartphone_s23 + smartphone_2 == 1200000.0


def test_add_different_classes_raises_type_error(product_iphone: Product, smartphone_s23: Smartphone) -> None:
    """Проверка запрета сложения объектов разных классов."""
    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов!"):
        _ = product_iphone + smartphone_s23


def test_lawn_grass_attributes() -> None:
    """Проверка инициализации специфичных свойств класса LawnGrass."""
    grass = LawnGrass(
        name="Трава",
        description="Мягкая",
        price=150.0,
        quantity=10,
        country="Нидерланды",
        germination_period="5 дней",
        color="Салатовый",
    )
    assert grass.country == "Нидерланды"
    assert grass.germination_period == "5 дней"
    assert grass.color == "Салатовый"
