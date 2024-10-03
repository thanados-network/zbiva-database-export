from typing import Any

from citation import Citation


class Place:
    def __init__(self, data: dict[str, str]):
        self.id_ = data['id']
        self.begin = data['begin']
        self.end = data['end']
        self.name = data['name']
        self.admin_settlement = data['admin_settlement']
        self.admin_unit = data['admin_unit']
        self.admin_district = data['admin_district']
        self.admin_state = data['admin_state']
        self.admin_state2 = data['admin_state2']
        self.first_publication = data['first_publication']
        self.location_precision = data['location_precision']
        self.coordinate = data['coordinate']
        self.location_description = data['location_description']
        self.plot_number = data['plot_number']
        self.data_quality = data['data_quality']
        self.archaeological_quality = data['archaeological_quality']
        self.special_finds = data['special_finds']
        self.comments = data['comments']
        self.primary_chronology = data['primary_chronology']
        self.certainty_of_chronology = data['certainty_of_chronology']
        self.chronology_description = data['chronology_description']
        self.description = data['description']
        self.description_2 = data['description_2']
        self.summary = data['summary']
        self.primary_type_id = data['primary_type_id']
        self.citations: list[str] = []
        self.zbiva_types: list[str] = []
        self.openatlas_types: list[int] = []

    def __repr__(self) -> str:
        return str(self.__dict__)

    def get_citations(self, citations: list[Citation]) -> None:
        for citation in citations:
            if citation.place_id == self.id_:
                self.citations.append(citation.get_csv_data())

    def get_csv_data(self) -> dict[str, Any]:
        return {
            'id': self.id_,
            'name': self.name,
            'description': self.description,
            'references': ' '.join(self.citations),
            'type_ids': [],  # todo: get types
        }

    def map_types(self, types: dict[str, dict[str, Any]]):
        for type_code in self.zbiva_types:
            self.openatlas_types.append(types.get(type_code))
        # todo: doesn't seem to work. duplication in list?
        print(self.openatlas_types)
