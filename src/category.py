from typing import List

from src.product import Product


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += sum(product.quantity for product in products)

    def add_product(self, product: Product) -> None:
        self.__products.append(product)
        Category.product_count += product.quantity

    @property
    def products(self) -> str:
        result = ""
        for product in self.__products:
            result += f"{product.name}, {int(product.price)} руб. Остаток: {product.quantity} шт.\n"
        return result

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
