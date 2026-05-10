import json
from pathlib import Path
from typing import List

from src.category import Category
from src.utils import read_json


def test_read_json_success(tmp_path: Path) -> None:
    data = [
        {
            "name": "Смартфоны",
            "description": "Тест",
            "products": [{"name": "Iphone", "description": "X", "price": 1000.0, "quantity": 1}],
        }
    ]

    p = tmp_path / "products.json"
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    result: List[Category] = read_json(str(p))

    assert len(result) == 1
    assert isinstance(result[0], Category)
    assert result[0].name == "Смартфоны"
    assert "Iphone" in result[0].products


def test_read_json_empty(tmp_path: Path) -> None:
    p = tmp_path / "empty.json"
    p.write_text(json.dumps([]), encoding="utf-8")

    result: List[Category] = read_json(str(p))
    assert result == []
