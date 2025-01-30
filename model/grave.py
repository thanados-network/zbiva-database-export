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
        self.type_id = data.get("type_id")
        self.citations: list[str] = []

    def __repr__(self) -> str:
        return str(self.__dict__)

    def get_citations(self, citations: list[Citation]) -> None:
        for citation in citations:
            if citation.place_id == self.id_:
                self.citations.append(citation.get_csv_data())

    def get_csv_data(self) -> dict[str, Any]:
        return {
            'id': self.id_,
            'name': self.grave_label or '',
            'description': '',
            # 'type_ids': ' '.join(self.openatlas_types),
            'wkt': f"{self.coordinates}" if self.coordinates else '',
            'begin_from': f'{self.earliest}-01-01' if self.earliest else '',
            'begin_to': f'{self.earliest}-12-31' if self.earliest else '',
            'end_from': f'{self.latest}-01-01' if self.latest else '',
            'end_to': f'{self.latest}-12-31' if self.latest else '',
            'origin_reference_ids': f"{' '.join(self.citations)}",
            'parent_id': self.site_id,
            'openatlas_class': 'Feature'
        }
