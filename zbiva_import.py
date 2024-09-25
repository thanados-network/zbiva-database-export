from typing import Any

from literature import Literature
from sql import get_citation, get_literature, get_places, get_types


def get_literature_csv(data: list[Literature]) -> list[dict[str, str | Any]]:
    return [{'id': lit.id,
             'name': lit.name,
             'type_ids': lit.type_ids,
             'description': lit.description} for lit in data]


if __name__ == "__main__":
    types = get_types()
    literature = get_literature()
    places = get_places()
    citation = get_citation()

    literature_csv = get_literature_csv(literature)
    # print(json.dumps(data, ensure_ascii=False).encode('utf8'))
    # print(len(literature_csv))
    # print(literature_csv)
