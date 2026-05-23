from typing import List

from src.product import Product


class Category:
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: list) -> None:
        self.name = name
        self.description = description

        self.__products: List[Product] = []

        Category.category_count += 1

        for product in products:
            self.add_product(product)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только продукты или их наследников!")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[str]:
        return [str(product) for product in self.__products]

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
