from typing import Any

from model.citation import Citation


class Artifact:
    def __init__(
            self,
            data: dict[str, Any],
            gave_body_mapping: dict[str, Any]) -> None:
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

        # New relational data
        self.grave_ids = data.get("grave_ids")
        self.body_id = gave_body_mapping.get(f'grave_{self.grave_ids}')
        self.place_id = data.get("place_id")

        self.ostalo = data.get("has_ostalo")
        self.jagoda = data.get("has_jagoda")
        self.naglavniobrocek = data.get("has_naglavniobrocek")
        self.noz = data.get("has_noz")
        self.posoda = data.get("has_posoda")
        self.prstan = data.get("has_prstan")
        self.zaponka = data.get("has_zaponka")

        self.material = data.get("material")
        self.position = data.get("position")
        self.bead_color = data.get("bead_color")
        self.bead_ornament = data.get("bead_ornament")
        self.bead_glass = data.get("bead_glass")
        self.knife_sheath = data.get("knife_sheath")
        self.vessel_manufacture = data.get("vessel_manufacture")
        self.vessel_impression = data.get("vessel_impression")
        self.vessel_preserved_part = data.get("vessel_preserved_part")
        self.vessel_ornament = data.get("vessel_ornament")
        self.vessel_temper_type = data.get("vessel_temper_type")
        self.citations: list[str] = []

        # Collect all type codes from relational fields
        self.artifact_types: list[str] = []
        type_fields = [
            "material", "position", "bead_color", "bead_ornament",
            "bead_glass",
            "knife_sheath", "vessel_manufacture", "vessel_impression",
            "vessel_preserved_part", "vessel_ornament", "vessel_temper_type",
            "vessel_break_color", "vessel_inner_color", "vessel_outer_color",
            "vessel_burnt_residue", "vessel_rim_type", "vessel_temper_size",
            "vessel_type", "vessel_temper_content",
            "bead_cross_section", "bead_ground_plan",
            "headband_shape", "headband_twist",
            "knife_handle", "knife_back_shape", "knife_back_transition",
            "knife_blood_groove", "knife_tip", "knife_tang_shape",
            "knife_blade_shape", "knife_blade_transition", "knife_blade",
            "ring_shape", "buckle_shape", "preservation_id", "environment_id",
            "type_id"
            ]
        for field in type_fields:
            val = data.get(field)
            if val:
                # Split by comma (from STRING_AGG) and strip whitespace
                codes = [c.strip() for c in str(val).split(',')]
                for code in codes:
                    if code and code not in self.artifact_types:
                        self.artifact_types.append(code)

        self.openatlas_types: list[str] = ['239450']
        self.openatlas_value_types: list[tuple[str, Any]] = []
        self.reference_system_zbiva = self._get_reference_system_zbiva()

    def __repr__(self) -> str:
        return str(self.__dict__)

    def _get_reference_system_zbiva(self) -> str:
        artifact_type = "predmet"
        if self.ostalo:
            artifact_type = "ostalo"
        elif self.jagoda:
            artifact_type = "jagoda"
        elif self.naglavniobrocek:
            artifact_type = "naglavni_obrocek"
        elif self.noz:
            artifact_type = "noz"
        elif self.posoda:
            artifact_type = "posoda"
        elif self.prstan:
            artifact_type = "prstan"
        elif self.zaponka:
            artifact_type = "zaponka"
        return f"predmet/{artifact_type}/{self.id_};exact_match"

    def get_citations(self, citations: list[Citation]) -> None:
        for citation in citations:
            if citation.linked_id == self.id_:
                self.citations.append(citation.get_csv_data())

    def get_csv_data(self) -> dict[str, Any]:
        parent_id = None
        if self.body_id:
            parent_id = f'{self.body_id}'
        elif self.grave_ids:
            # If multiple grave_ids are present, we take the first one
            first_grave_id = str(self.grave_ids).split(',')[0].strip()
            parent_id = f'grave_{first_grave_id}'
        elif self.place_id:
            parent_id = f'site_{self.place_id}'

        return {
            'id': f'artifact_{self.id_}',
            'name': self.internal_label or 'Unlabeled',
            'description': self.notes,
            'type_ids': ' '.join(
                t for t in self.openatlas_types if t != 'None'),
            'value_types': ' '.join(
                [f'{t};{v}' for t, v in self.openatlas_value_types]),
            'wkt': f"{self.coordinates}" if self.coordinates else '',
            'begin_from': f'{self.earliest:04}-01-01' if self.earliest else
            None,
            'begin_to': f'{self.earliest:04}-12-31' if self.earliest else None,
            'end_from': f'{self.latest:04}-01-01' if self.latest else None,
            'end_to': f'{self.latest:04}-12-31' if self.latest else None,
            'origin_reference_ids': f"{' '.join(self.citations)}",
            'body_id': self.body_id,
            'place_id': self.place_id,
            'parent_id': parent_id,
            'reference_system_zbiva': self.reference_system_zbiva,
            'openatlas_class': 'artifact'}

    def map_types(self, types: dict[str, int]) -> None:
        for type_code in self.artifact_types:
            atlas_id = types.get(type_code)
            if atlas_id:
                atlas_id_str = str(atlas_id)
                if atlas_id_str not in self.openatlas_types:
                    self.openatlas_types.append(atlas_id_str)

    def map_value_types(self) -> None:
        if self.number_of_pieces:
            self.openatlas_value_types.append(
                ('284626', self.number_of_pieces))
        if self.length:
            self.openatlas_value_types.append(('26189', self.length))
        if self.width:
            self.openatlas_value_types.append(('26188', self.width))
        if self.thickness:
            self.openatlas_value_types.append(('26187', self.thickness))
        if self.weight:
            self.openatlas_value_types.append(('26186', self.weight))
