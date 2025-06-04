from typing import Any

import requests


def get_type_tree_thanados() -> dict[str, dict[str, Any]]:
    return requests.get(
        'https://thanados.openatlas.eu/api/type_tree/',
        timeout=60).json()
