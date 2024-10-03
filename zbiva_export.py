from collections import defaultdict
from typing import Any

from mypy.checkmember import type_object_type

from api import get_type_tree_thanados
from citation import Citation
from literature import Literature
from place import Place
from sql import (
    fetch_site_cult_types, fetch_site_finds_types, fetch_site_grave_types,
    fetch_site_other_types, fetch_site_settlement_types,
    fetch_site_topography_types, fetch_site_depot_types,
    get_place_citation_from_database,
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



def get_place_literature(
        lit: list[Literature],
        cit: list[Citation]) -> list[Literature]:
    place_citation_lit_ids = {c.origin_literature_id for c in cit}
    return [l for l in lit if l.id_ in place_citation_lit_ids]



def get_thanados_types():
    type_tree = get_type_tree_thanados()['typeTree']
    result = {}

    def recurse_subs(entry_id: str):
        entry = type_tree.get(str(entry_id))
        if not entry:
            return

        result[entry['description']] = entry['id']

        subs = entry.get('subs', [])
        for sub_id in subs:
            recurse_subs(sub_id)

    recurse_subs('237367')  # This is the OpenAtlas ID of Zbiva types
    return result


if __name__ == "__main__":
    # types_names = get_type_names_from_database()
    literature = get_literature_from_database()
    citations = get_place_citation_from_database()
    types = get_type_codes_for_sites()
    thanados_types = get_thanados_types()


    places = get_places_from_database()
    for place in places:
        place.get_citations(citations)
        place.zbiva_types.extend(types[place.id_])
        place.map_types(thanados_types)


    place_literature = get_place_literature(literature, citations)
    literature_csv = [lit.get_csv_data() for lit in place_literature]

    # Get only slovenian places
    sorted_places_by_country = sort_places_by_country(places)

    sorted_places_by_type = defaultdict(list)
    for i in sorted_places_by_country['slovenija']:
        sorted_places_by_type[i.primary_type_id].append(i)

    print(len(sorted_places_by_type['NVR02']))


    # print(json.dumps(data, ensure_ascii=False).encode('utf8'))
