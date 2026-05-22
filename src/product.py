from typing import Any, Dict, List, Optional


class Product:

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self._price

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
    def new_product(
        cls, data: Dict[str, Any], products_list: Optional[List["Product"]] = None
    ) -> "Product":
        name = data.get("name", "")
        description = data.get("description", "")
        price = float(data.get("price", 0.0))
        quantity = int(data.get("quantity", 0))

        if products_list:
            for product in products_list:
                if product.name == name:
                    product.quantity += quantity
                    product._price = max(product.price, price)
                    return product

        return cls(name, description, price, quantity)

    def __str__(self) -> str:
        return f"{self.name}, {int(self.price)} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Any) -> Any:
        if not isinstance(other, Product):
            return NotImplemented

        current_total = self.price * self.quantity
        other_total = other.price * other.quantity
        return current_total + other_total
