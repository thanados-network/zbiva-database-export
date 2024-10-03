from typing import Any

import requests

from globals import API_URL


def get_type_tree_thanados() -> dict[str, dict[str, Any]]:
    return requests.get(f'{API_URL}/type_tree/').json()


