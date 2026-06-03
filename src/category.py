from abc import ABC, abstractmethod
from typing import List

from src.product import Product


class BaseCategoryOrder(ABC):
    """Абстрактный базовый класс для категорий и заказов."""

    def __init__(self) -> None:
        pass

    @property
    @abstractmethod
    def total_quantity(self) -> int:#
        pass

    @property
    @abstractmethod
    def total_cost(self) -> float:
        pass


class Category(BaseCategoryOrder):
    """Класс для представления категории продуктов."""

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: list) -> None:
        super().__init__()

        for product in products:
            if not isinstance(product, Product):
                raise TypeError("Можно добавлять только продукты или их наследников!")

        self.name = name
        self.description = description
        self.__products: List[Product] = []

        Category.category_count += 1

        for product in products:
            self.add_product(product)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию и увеличивает глобальный счетчик."""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только продукты или их наследников!")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[str]:
        """Возвращает список строковых представлений продуктов."""
        return [str(product) for product in self.__products]

    @property
    def total_quantity(self) -> int:
        """Возвращает общее количество всех продуктов в категории."""
        return sum(product.quantity for product in self.__products)

    @property
    def total_cost(self) -> float:
        """Возвращает общую стоимость всех продуктов в категории."""
        return sum(product.price * product.quantity for product in self.__products)

    def __str__(self) -> str:
        return f"{self.name}, количество продуктов: {self.total_quantity} шт."


class Order(BaseCategoryOrder):
    """Класс для представления заказа конкретного продукта."""

    def __init__(self, product: Product, quantity: int) -> None:
        super().__init__()
        if not isinstance(product, Product):
            raise TypeError("В заказ можно добавить только продукт или его наследника!")
        self.product = product
        self.quantity = quantity

    @property
    def total_quantity(self) -> int:
        """Возвращает количество товара в заказе."""
        return self.quantity

    @property
    def total_cost(self) -> float:
        """Возвращает полную стоимость заказа."""
        return float(self.product.price * self.quantity)

    def __str__(self) -> str:
        return f"Заказ: {self.product.name} x {self.quantity} шт. Итоговая стоимость: {int(self.total_cost)} руб."
