from sql import (
    get_citation_from_database, get_literature_from_database,
    get_places_from_database, get_types_from_database)

if __name__ == "__main__":
    types = get_types_from_database()
    literature = get_literature_from_database()
    places = get_places_from_database()
    citations = get_citation_from_database()
    for place in places:
        place.get_citations(citations)

    literature_csv = [lit.get_csv_data() for lit in literature]
    # print(json.dumps(data, ensure_ascii=False).encode('utf8'))
    # print(len(literature_csv))
    # print(literature_csv)
