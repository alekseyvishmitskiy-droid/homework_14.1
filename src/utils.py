import json
import os

from src.category import Category
from src.product import Product


def read_json(path: str) -> list:

    full_path = os.path.abspath(path)

    with open(full_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []

    for category_data in data:
        products = []
        for prod_data in category_data.get("products", []):
            products.append(
                Product(
                    name=prod_data["name"],
                    description=prod_data["description"],
                    price=prod_data["price"],
                    quantity=prod_data["quantity"],
                )
            )

        categories.append(
            Category(name=category_data["name"], description=category_data["description"], products=products)
        )

    return categories


if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(category1.products)
    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)
    print(category1.products)
    print(category1.product_count)

    new_product = Product.new_product(
        {"name": "Samsung Galaxy S23 Ultra", "description": "256GB, Серый цвет, 200MP камера", "price": 180000.0,
         "quantity": 5})
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    new_product.price = 800
    print(new_product.price)

    new_product.price = -100
    print(new_product.price)
    new_product.price = 0
    print(new_product.price)
