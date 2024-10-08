from collections import defaultdict
from typing import Any

from api import get_type_tree_thanados
from citation import Citation
from literature import Literature
from place import Place
from sql import (
    get_literature_from_database,
    get_place_citation_from_database, get_places_from_database)


def sort_places_by_country(places_: list[Place]) -> dict[str, Any]:
    countries = defaultdict(list)
    for place_ in places_:
        countries[place_.admin_state2].append(place_)
    return countries



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
    thanados_types = get_thanados_types()


    places = get_places_from_database()
    for place in places:
        place.get_citations(citations)
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


def test_which_other_types_exist():
    # Get overview of some types:
    location_precision = set()
    plot_number = set()
    data_quality = set()
    archaeological_quality = set()
    special_finds = set()
    primary_chronology = set()
    certainty_of_chronology = set()
    chronology_description = set()
    location_description = set()
    author_of_site = set()
    for place in sorted_places_by_country['slovenija']:
        location_precision.add(place.location_precision)
        plot_number.add(place.plot_number)
        data_quality.add(place.data_quality)
        archaeological_quality.add(place.archaeological_quality)
        special_finds.add(place.special_finds)
        primary_chronology.add(place.primary_chronology)
        certainty_of_chronology.add(place.certainty_of_chronology)
        chronology_description.add(place.chronology_description)
        location_description.add(place.location_description)
        author_of_site.add(place.author_of_site)

    print(location_precision)
    print(plot_number)
    print(data_quality)
    print(archaeological_quality)
    print(special_finds)
    print(primary_chronology)
    print(certainty_of_chronology)
    print(chronology_description)
    print(location_description)
    print(author_of_site)
