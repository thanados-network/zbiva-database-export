from typing import Any

from model.citation import Citation

prime_type_mapping = {
    'NVR00': 'ostalo',
    'NVR01': 'naselbina',
    'NVR02': 'grobisce',
    'NVR03': 'zakladna_najdba',
    'NVR04': 'kultni_prostor',
    'NVR05': 'ostalo',
    'NVR06': 'ostalo',
    'NVR07': 'ostalo',
}


class Place:
    def __init__(self, data: dict[str, Any]):
        self.id_ = data['id']
        self.begin = data['begin']
        self.end = data['end']
        self.name = data['name'] or 'Unknown'
        self.admin_settlement = data['admin_settlement']
        self.admin_unit = data['admin_unit']
        self.admin_area = data['admin_area']
        self.admin_region = data['admin_region']
        self.admin_country = data['admin_country']
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
        self.author_of_site = data['author_of_site']
        self.chronology_description = data['chronology_description']
        self.description = data['description']
        self.description_2 = data['description_2']
        self.summary = data['summary']
        self.primary_type_id = data['primary_type_id']
        self.reference_system_zbiva = (
            f'najdisce/{prime_type_mapping[self.primary_type_id]}/'
            f'{self.id_};exact_match')
        self.citations: list[str] = []
        self.site_types: list[str] = self.get_all_site_types(data)
        self.openatlas_types: list[str] = ['239450']

    def __repr__(self) -> str:
        return str(self.__dict__)

    def get_all_site_types(self, data: dict[str, Any]) -> list[str]:
        types = data['site_types']
        if loc := self.location_precision:
            types.append(f"lokacije_{loc}")
        if chrono := self.certainty_of_chronology:
            types.append(f"datacije_{chrono}")
        if prime := self.primary_chronology:
            types.append(prime)
        if archeological := self.archaeological_quality:
            types.append(f"poda_{archeological}")
        if quality := self.data_quality:
            types.append(quality)
        return types

    def get_citations(self, citations: list[Citation]) -> None:
        for citation in citations:
            if citation.linked_id == self.id_:
                self.citations.append(citation.get_csv_data())

    def get_csv_data(self) -> dict[str, Any]:
        return {
            'id': f'site_{self.id_}',
            'name': self.name or 'Unknown',
            'description': f"{self.description}" if self.description else '',
            'type_ids': ' '.join(
                t for t in self.openatlas_types if t != 'None'),
            'value_types': '',
            'wkt': f"{self.coordinate}" if self.coordinate else '',
            'begin_from': f'{self.begin}-01-01' if self.begin else '',
            'begin_to': f'{self.begin}-12-31' if self.begin else '',
            'end_from': f'{self.end}-01-01' if self.end else '',
            'end_to': f'{self.end}-12-31' if self.end else '',
            'origin_reference_ids': f"{' '.join(self.citations)}",
            'parent_id': '',
            'openatlas_class': 'Place',
            'reference_system_zbiva': self.reference_system_zbiva,
            'region': self.admin_area,
            'district': self.admin_unit,
            'cadastre': self.admin_settlement}

    def map_types(self, types: dict[str, int]) -> None:
        for type_code in self.site_types + [self.primary_type_id]:
            self.openatlas_types.append(str(types.get(type_code)))
