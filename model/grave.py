from typing import Any


class Grave:
    def __init__(self, data: dict[str, Any]):
        self.id = data.get("id")
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

