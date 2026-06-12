import json
import os
from typing import List

from src.category import Category
from src.product import Product


def read_json(path: str) -> List[Category]:
    """Считывает JSON-файл и инициализирует объекты категорий и продуктов."""
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
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы "
            f"при попытке добавить продукт с нулевым количеством: {e}"
        )
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())
