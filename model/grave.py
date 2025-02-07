from typing import Any

from model.citation import Citation


class Grave:
    def __init__(self, data: dict[str, Any]):
        self.id_ = data.get("id")
        self.entry_date = data.get("entry_date")
        self.modification_date = data.get("modification_date")
        self.entered_by = data.get("entered_by")
        self.earliest = data.get("earliest")
        self.latest = data.get("latest")
        self.author = data.get("author")
        self.coordinates = data.get("coordinates")
        self.grave_label = data.get("grave_label")
        self.number_of_deceased = data.get("number_of_deceased")
        self.grave_length = data.get("grave_length")
        self.grave_width = data.get("grave_width")
        self.depth_from = data.get("depth_from")
        self.depth_to = data.get("depth_to")
        self.deviation_from_north = data.get("deviation_from_north")
        self.deviation_description = data.get("deviation_description")
        self.coffin_length = data.get("coffin_length")
        self.coffin_width = data.get("coffin_width")
        self.notes = data.get("notes")
        self.site_id = data.get("site_id")
        self.primary_type_id = data.get("type_id")
        self.citations: list[str] = []
        self.grave_types: list[str] = data['grave_types']
        self.openatlas_types: list[str] = ['239450']
        self.openatlas_value_types: list[tuple[str, Any]] = []

    def __repr__(self) -> str:
        return str(self.__dict__)

    def get_citations(self, citations: list[Citation]) -> None:
        for citation in citations:
            if citation.linked_id == self.id_:
                self.citations.append(citation.get_csv_data())

    def get_csv_data(self) -> dict[str, Any]:
        return {
            'id': self.id_,
            'name': self.grave_label or '',
            'description': self.notes,
            'type_ids': ' '.join(self.openatlas_types),
            'value_types': ' '.join(
                [f'{t};{v}' for t, v in self.openatlas_value_types]),
            'wkt': f"{self.coordinates}" if self.coordinates else '',
            'begin_from': f'{self.earliest}-01-01' if self.earliest else '',
            'begin_to': f'{self.earliest}-12-31' if self.earliest else '',
            'end_from': f'{self.latest}-01-01' if self.latest else '',
            'end_to': f'{self.latest}-12-31' if self.latest else '',
            'origin_reference_ids': f"{' '.join(self.citations)}",
            'parent_id': self.site_id,
            'openatlas_class': 'Feature'
        }

    def map_types(self, types: dict[str, int]) -> None:
        own_types = self.grave_types
        if self.primary_type_id:
            own_types += [self.primary_type_id]
        for type_code in own_types:
            self.openatlas_types.append(str(types.get(type_code)))

    def map_value_types(self):
        if self.number_of_deceased:
            self.openatlas_value_types.append(
                ('256001', self.number_of_deceased))
        if self.grave_length:
            self.openatlas_value_types.append(('26189', self.grave_length))
        if self.grave_width:
            self.openatlas_value_types.append(('26188', self.grave_width))
        if self.depth_from:
            self.openatlas_value_types.append(('256032', self.depth_from))
        if self.depth_to:
            self.openatlas_value_types.append(('256031', self.depth_to))
        if self.deviation_from_north:
            self.openatlas_value_types.append(
                ('118730', self.deviation_from_north))
        if self.coffin_length:
            self.openatlas_value_types.append(('256029', self.coffin_length))
        if self.coffin_width:
            self.openatlas_value_types.append(('256030', self.coffin_width))
