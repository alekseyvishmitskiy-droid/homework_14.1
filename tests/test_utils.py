import json
import pytest
from src.utils import read_json
from src.category import Category


def test_read_json_success(tmp_path):
    data = [
        {
            "name": "Смартфоны",
            "description": "Тест",
            "products": [
                {"name": "Iphone", "description": "X", "price": 1000.0, "quantity": 1}
            ]
        }
    ]


    p = tmp_path / "products.json"
    p.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')


    result = read_json(str(p))

    assert len(result) == 1
    assert isinstance(result[0], Category)
    assert result[0].name == "Смартфоны"
    assert result[0].products[0].name == "Iphone"


def test_read_json_empty(tmp_path):
    p = tmp_path / "empty.json"
    p.write_text(json.dumps([]), encoding='utf-8')

    result = read_json(str(p))
    assert result == []

