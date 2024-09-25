from typing import Any

from pydantic.fields import defaultdict

from place import Place
from sql import (
    get_citation_from_database, get_literature_from_database,
    get_places_from_database, get_types_from_database)


def sort_places_by_country(places_: list[Place]) -> dict[str, Any]:
    countries = {
        'austria': [],
        'slovenia': [],
        'other': []}
    for place_ in places_:
        match place_.admin_state2:
            case 'avstrija':
                countries['austria'].append(place_)
            case 'slovenija':
                countries['slovenia'].append(place_)
            case _:
                countries['other'].append(place_)
    return countries


if __name__ == "__main__":
    types = get_types_from_database()
    literature = get_literature_from_database()
    places = get_places_from_database()
    citations = get_citation_from_database()
    for place in places:
        place.get_citations(citations)

    literature_csv = [lit.get_csv_data() for lit in literature]

    # Get only slovenian places
    sorted_places_by_country = sort_places_by_country(places)

    sorted_places_by_type = defaultdict(list)
    for i in sorted_places_by_country['slovenia']:
        sorted_places_by_type[i.primary_type_id].append(i)

    print(len(sorted_places_by_type['NVR02']))




    # print(json.dumps(data, ensure_ascii=False).encode('utf8'))
