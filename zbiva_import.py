from typing import Any

import psycopg2

from globals import DB_PARAMETER
from literature import Literature
from sql import get_literature, get_places, get_types


def get_data() -> dict[str, Any]:
    try:
        with psycopg2.connect(**DB_PARAMETER) as conn:
            with conn.cursor() as cursor:
                return {
                    "types": get_types(cursor),
                    "literature": get_literature(cursor),
                    "places": get_places(cursor)}

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return {}


def get_literature_csv(data_: list[Literature]) -> list[dict[str, str | Any]]:
    return [{'id': lit.id_,
             'name': lit.name,
             'type_ids': lit.type_ids,
             'description': lit.description} for lit in data_]


if __name__ == "__main__":
    data = get_data()
    literature_csv = get_literature_csv(data['literature'])
    # print(json.dumps(data, ensure_ascii=False).encode('utf8'))
    # print(len(literature_csv))
    # print(literature_csv)

# todo: Get only the literature we need for sites
