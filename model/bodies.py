from typing import Any

from model.citation import Citation


class Body:
    def __init__(self, data: dict):
        self.id_ = data.get("id")
        self.entry_date = data.get("entry_date")  # not used
        self.modification_date = data.get("modification_date")  # not used
        self.entered_by = data.get("entered_by")  # not used
        self.earliest = data.get("earliest")
        self.latest = data.get("latest")
        self.author = data.get("author")  # not used
        self.coordinates = data.get("coordinates")
        self.star_id = data.get("star_id")
        self.label = data.get("label")
        self.min_age = data.get("min_age")  # value type
        self.max_age = data.get("max_age")  # value type
        self.notes = data.get("notes")
        self.grave_id = data.get("grave_id")
        self.right_hand_position_id = data.get("right_hand_position_id")
        self.head_position_id = data.get("head_position_id")
        self.left_hand_position_id = data.get("left_hand_position_id")
        self.legs_position_id = data.get("legs_position_id")
        self.body_position_id = data.get("body_position_id")
        self.special_features_id = data.get("special_features_id")
        self.additions_id = data.get("additions_id")
        self.gender_id = data.get("gender_id")
        self.reference_system_zbiva = f'telo/{self.id_};exact_match'
        self.citations: list[str] = []
        self.openatlas_types: list[str] = ['239450']
        self.body_types = self.get_body_types()
        self.openatlas_value_types: list[tuple[str, Any]] = []

    def __repr__(self) -> str:
        return str(self.__dict__)

    def get_csv_data(self) -> dict[str, Any]:
        return {
            'id': f'body_{self.id_}',
            'name': self.label or 'Unmarked',
            'description': self.notes,
            'type_ids': ' '.join(
                t for t in self.openatlas_types if t != 'None'),
            'value_types': ' '.join(
                [f'{t};{v}' for t, v in self.openatlas_value_types]),
            'wkt': f"{self.coordinates}" if self.coordinates else '',
            'begin_from': f'{self.earliest}-01-01' if self.earliest else '',
            'begin_to': f'{self.earliest}-12-31' if self.earliest else '',
            'end_from': f'{self.latest}-01-01' if self.latest else '',
            'end_to': f'{self.latest}-12-31' if self.latest else '',
            'origin_reference_ids': f"{' '.join(self.citations)}",
            'parent_id': f'grave_{self.grave_id}',
            'reference_system_zbiva': self.reference_system_zbiva,
            'openatlas_class': 'Stratigraphic unit'}

    def get_citations(self, citations: list[Citation]) -> None:
        for citation in citations:
            if citation.linked_id == self.id_:
                self.citations.append(citation.get_csv_data())

    def map_types(self, types: dict[str, int]) -> None:
        for type_code in self.body_types:
            self.openatlas_types.append(str(types.get(type_code)))

    def get_body_types(self) -> list[str]:
        return [
            self.right_hand_position_id,
            self.head_position_id,
            self.left_hand_position_id,
            self.legs_position_id,
            self.body_position_id,
            self.special_features_id,
            self.additions_id,
            self.gender_id]

    def map_value_types(self):
        if self.min_age:
            self.openatlas_value_types.append(('117199', self.min_age))
        if self.max_age:
            self.openatlas_value_types.append(('117200', self.max_age))
