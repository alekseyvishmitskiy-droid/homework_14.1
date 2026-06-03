from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, cast


class LogMixin:
    """Миксин для логирования процесса создания объектов."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        print(f"Был создан объект: {self.__repr__()}")

    def __repr__(self) -> str:
        attrs = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in self.__dict__.values()])
        return f"{self.__class__.__name__}({attrs})"


class BaseProduct(ABC):
    """Базовый абстрактный класс для всех продуктов."""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self) -> str:
        """Абстрактный метод для строкового представления (обязателен для реализации)."""
        pass

    @abstractmethod
    def __add__(self, other: Any) -> float:
        """Абстрактный метод для сложения продуктов (обязателен для реализации)."""
        pass


class Product(LogMixin, BaseProduct):
    """Базовый класс конкретных продуктов."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        super().__init__(name, description, price, quantity)

    @property
    def price(self) -> float:
        return float(self._price)

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if new_price < self._price:
            user_answer = input("Цена снижается. Подтвердить? (y/n): ")
            if user_answer.lower() == "y":
                self._price = new_price
        else:
            self._price = new_price

    @classmethod
    def new_product(cls, data: Dict[str, Any], products_list: Optional[List["Product"]] = None) -> "Product":
        name = data.get("name", "")
        description = data.get("description", "")
        price = float(data.get("price", 0.0))
        quantity = int(data.get("quantity", 0))

        if products_list:
            for product in products_list:
                if product.name == name:
                    product.quantity += quantity
                    product._price = max(product._price, price)
                    return cast(Product, product)

        extra_kwargs = {k: v for k, v in data.items() if k not in ["name", "description", "price", "quantity"]}
        return cls(name, description, price, quantity, **extra_kwargs)

    def __str__(self) -> str:
        return f"{self.name}, {int(self.price)} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Any) -> float:
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов!")

        current_total = float(self.price) * int(self.quantity)
        other_total = float(other.price) * int(other.quantity)

        return float(current_total + other_total)


class Smartphone(Product):
    """Класс Смартфон."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        super().__init__(name, description, price, quantity)


class LawnGrass(Product):
    """Класс Трава газонная."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        self.country = country
        self.germination_period = germination_period
        self.color = color
        super().__init__(name, description, price, quantity)
