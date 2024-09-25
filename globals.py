CSV_TEMPLATE = {
    'id': '',
    'name': '',
    'alias': '',
    'description': '',
    'begin_from': '',
    'begin_to': '',
    'begin_comment': '',
    'end_from': '',
    'end_to': '',
    'end_comment': '',
    'wkt': '',
    'type_ids': '',
    'value_types': '',
    'reference_system_wikidata': '',
    'reference_system_geonames': '',
    'administrative_unit': '',
    'historical_place': '',
    'openatlas_class': '',
    'parent_id': '',
    'openatlas_parent_id': ''}

TYPE_TABLES = [
    'lastnosti_najdisc_grobisceoddaljenost',
    'lastnosti_najdisc_grobiscepokop',
    'lastnosti_najdisc_grobisceprostor',
    'lastnosti_najdisc_grobiscetip',
    'lastnosti_najdisc_grobisceusmerjenost',
    'lastnosti_najdisc_grobiscevelikost',
    'lastnosti_najdisc_kultniprostortip',
    'lastnosti_najdisc_najdba',
    'lastnosti_najdisc_naselbinatip',
    'lastnosti_najdisc_naselbinautrjenost',
    'lastnosti_najdisc_naselbinavelikost',
    'lastnosti_najdisc_naselbinavrstesledov',
    'lastnosti_najdisc_primarnakategorija',
    'lastnosti_najdisc_topografskalega',
    'lastnosti_najdisc_zakladnanajdbaobmocje']

SITE_TABLES = ['najdisca_najdisce']

SITE_TYPES = [
    'najdisca_kultniprostor',
    'najdisca_najdisce_najdbe',
    'najdisca_najdisce_topografske_lege',
    'najdisca_ostalo',  # has only najdisce_id!!! ostalo means other!
    'najdisca_zakladnanajdba']

SITE_SPECIAL_TYPES = [
    'najdisca_grobisce',
    'najdisca_naselbina']

SITE_CITATION = ['najdisca_najdisceliteratura']
