from contextlib import closing
from typing import Any

import psycopg2

from globals import DB_PARAMETER
from literature import Literature
from sql import get_literature, get_types


def get_data() -> dict[str, Any]:
    try:
        with closing(psycopg2.connect(**DB_PARAMETER)) as conn:
            with closing(conn.cursor()) as cursor:
                types = get_types(cursor)
                literature = get_literature(cursor)

                return {
                    "types": types,
                    "literature": literature
                }

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return {}


def get_literature_csv(data_: list[Literature]) -> list[dict[str, str | Any]]:

    list_ = []
    for lit in data_:
        list_.append({
            'id': lit.id_,
            'name': lit.name,
            'type_ids': '5' if not lit.publication else '4',
            'description': lit.description

        })
    return list_


if __name__ == "__main__":
    data = get_data()
    literature_csv = get_literature_csv(data['literature'])
    # print(json.dumps(data, ensure_ascii=False).encode('utf8'))
    # print(literature_csv)
