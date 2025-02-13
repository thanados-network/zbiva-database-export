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


TYPES_BODIES_DICT = { # to add to the type tree in OpenAtlas
  "body_sex": [
    { "code": "TS002", "description": "male" },
    { "code": "TS001", "description": "female" }
  ],
  "body_appendages": [
    { "code": "TR003", "description": "no data" },
    { "code": "TR002", "description": "no visible appendages" },
    { "code": "TR001", "description": "has visible appendages" }
  ],
  "body_special_characteristics": [
    { "code": "TP003", "description": "other skeletal anomalies" },
    { "code": "TP001", "description": "deformed skull" },
    { "code": "TP002", "description": "skeletal injuries" }
  ],
  "body_preservation": [
    { "code": "TO004", "description": "in original position" },
    { "code": "TO002", "description": "partially preserved" },
    { "code": "TO006", "description": "all bones displaced" },
    { "code": "TO003", "description": "not preserved" },
    { "code": "TO005", "description": "partially displaced bones" },
    { "code": "TO001", "description": "preserved: at least long bones and skull" }
  ],
  "body_position": [
    { "code": "TLT02", "description": "right side - extended" },
    { "code": "TLT04", "description": "flexed on right side" },
    { "code": "TLT01", "description": "on back" },
    { "code": "TLT05", "description": "flexed on left side" },
    { "code": "TLT03", "description": "left side - extended" },
    { "code": "TLT06", "description": "different body position" }
  ],
  "leg_position": [
    { "code": "TLN03", "description": "different leg position" },
    { "code": "TLN01", "description": "parallel (legs)" },
    { "code": "TLN02", "description": "crossed (legs)" }
  ],
  "left_arm_position": [
    { "code": "TLRL04", "description": "different left arm position" },
    { "code": "TLRL05", "description": "left arm bent upward" },
    { "code": "TLRL03", "description": "left arm bent at a right angle" },
    { "code": "TLRL01", "description": "left arm extended" },
    { "code": "TLRL06", "description": "left arm folded" },
    { "code": "TLRL02", "description": "left arm partially bent" }
  ],
  "head_position": [
    { "code": "TLG02", "description": "right (head)" },
    { "code": "TLG03", "description": "left (head)" },
    { "code": "TLG04", "description": "different head position" },
    { "code": "TLG01", "description": "straight (head)" }
  ],
  "right_arm_position": [
    { "code": "TLRD06", "description": "right arm folded" },
    { "code": "TLRD03", "description": "right arm bent at a right angle" },
    { "code": "TLRD04", "description": "different right arm position" },
    { "code": "TLRD05", "description": "right arm bent upward" },
    { "code": "TLRD02", "description": "right arm partially bent" },
    { "code": "TLRD01", "description": "right arm extended" }
  ]
}
