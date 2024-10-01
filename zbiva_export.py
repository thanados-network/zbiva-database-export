from collections import defaultdict
from typing import Any

from place import Place
from sql import (
    fetch_site_cult_types, fetch_site_finds_types, fetch_site_grave_types,
    fetch_site_other_types, fetch_site_settlement_types,
    fetch_site_topography_types, fetch_site_depot_types,
    get_citation_from_database,
    get_literature_from_database,
    get_places_from_database, get_type_names_from_database)


def sort_places_by_country(places_: list[Place]) -> dict[str, Any]:
    countries = defaultdict(list)
    for place_ in places_:
        countries[place_.admin_state2].append(place_)
    return countries


def get_type_codes_for_sites() -> dict[str, list[str]]:
    site_types = {}
    site_types.update(fetch_site_grave_types())
    site_types.update(fetch_site_settlement_types())
    site_types.update(fetch_site_cult_types())
    site_types.update(fetch_site_other_types())
    site_types.update(fetch_site_depot_types())

    site_types.update(fetch_site_topography_types())
    site_types.update(fetch_site_finds_types())
    return site_types


if __name__ == "__main__":
    types_names = get_type_names_from_database()
    literature = get_literature_from_database()
    places = get_places_from_database()
    citations = get_citation_from_database()
    types = get_type_codes_for_sites()
    for place in places:
        place.get_citations(citations)
        place.types.extend(types[place.id_])

    literature_csv = [lit.get_csv_data() for lit in literature]

    # Get only slovenian places
    sorted_places_by_country = sort_places_by_country(places)

    sorted_places_by_type = defaultdict(list)
    for i in sorted_places_by_country['slovenija']:
        sorted_places_by_type[i.primary_type_id].append(i)

    print(len(sorted_places_by_type['NVR02']))

    # print(json.dumps(data, ensure_ascii=False).encode('utf8'))
