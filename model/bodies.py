class Body:
    def __init__(self, data: dict):
        self.id = data.get("id")
        self.entry_date = data.get("entry_date")
        self.modification_date = data.get("modification_date")
        self.entered_by = data.get("entered_by")
        self.earliest = data.get("earliest")
        self.latest = data.get("latest")
        self.author = data.get("author")
        self.coordinates = data.get("coordinates")
        self.star_id = data.get("star_id")
        self.label = data.get("label")
        self.min_age = data.get("min_age")
        self.max_age = data.get("max_age")
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

    def __repr__(self) -> str:
        return str(self.__dict__)


# Todo make the functions to create the csv files
