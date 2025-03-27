from typing import Any

from model.citation import Citation


class Artifact:
    def __init__(self, data: dict):
        self.id_ = data.get("id")
        self.entry_date = data.get("entry_date")
        self.modification_date = data.get("modification_date")
        self.entered_by = data.get("entered_by")
        self.earliest = data.get("earliest")
        self.latest = data.get("latest")
        self.author = data.get("author")
        self.coordinates = data.get("coordinates")
        self.star_id = data.get("star_id")
        self.stratigraphic_unit = data.get("stratigraphic_unit")
        self.internal_label = data.get("internal_label")
        self.original = data.get("original")
        self.number_of_pieces = data.get("number_of_pieces")
        self.primary_use = data.get("primary_use")
        self.length = data.get("length")
        self.width = data.get("width")
        self.thickness = data.get("thickness")
        self.weight = data.get("weight")
        self.other_measurements = data.get("other_measurements")
        self.notes = data.get("notes")
        self.site_id = data.get("site_id")
        self.preservation_id = data.get("preservation_id")
        self.environment_id = data.get("environment_id")
        self.type_id = data.get("type_id")
        self.citations: list[str] = []
        self.openatlas_types: list[str] = ['239450']
        self.artifact_types = self.get_artifact_types()
        self.openatlas_value_types: list[tuple[str, Any]] = []


    def __repr__(self) -> str:
        return str(self.__dict__)

    def get_artifact_types(self):
        pass


    def get_citations(self, citations: list[Citation]) -> None:
        for citation in citations:
            if citation.linked_id == self.id_:
                self.citations.append(citation.get_csv_data())
