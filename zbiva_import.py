import json
from contextlib import closing
from typing import Any

import psycopg2

db_params = {
    "dbname": "zbiva",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432}

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

# Includes site id and koda of type
# najdisce_id, tip_id
SITE_TYPES = [
    'najdisca_kultniprostor',
    'najdisca_najdisce_najdbe',
    'najdisca_najdisce_topografske_lege',
    'najdisca_ostalo',  # has nur najdisce_id!!! ostalo means other!
    'najdisca_zakladnanajdba']

SITE_SPECIAL_TYPES = [
    'najdisca_grobisce',
    'najdisca_naselbina']

SITE_CITATION = ['najdisca_najdisceliteratura']


def get_literature(cursor) -> list[dict[Any, Any]]:
    query = f"""
            SELECT
                id, 
                avtor AS autor,
                naslov AS title,
                publikacija AS publication,
                leto_objave AS date,
                kraj_objave AS location, 
                strani AS pages,
                signatura AS signature,
                pdf_link,
                doi
            FROM public.literatura_clanek
            """
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_types(cursor) -> dict[str, list[dict[str, str]]]:
    types = {}
    for table in TYPE_TABLES:
        query = f"""
                SELECT koda, opis
                FROM public.{table};
            """
        cursor.execute(query)
        types[table.replace('lastnosti_najdisc_', '')] = [
            {'koda': a[0], 'opis': a[1]} for a in cursor.fetchall()]
    return types


def get_data() -> dict[str, Any]:
    try:
        with closing(psycopg2.connect(**db_params)) as conn:
            with closing(conn.cursor()) as cursor:
                types = get_types(cursor)
                literature = get_literature(cursor)

                return {
                    "types": types,
                    "literature": literature
                }

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return {}


def get_literature_csv(data_: dict[str, Any]) -> dict[str, Any]:
    list_ = []
    for lit in data_:
        # Get name, problem is, if no Autor | publication | title exist
        if lit.get('autor'):
            name = f"{lit['autor'].split(' ')[0]} {lit['date']}"
        elif lit.get('publication'):
            name = f"{lit['publication'].split(' ')[0]} {lit['date']}"
        elif lit.get('title'):
            name = f"{lit['title'].split(' ')[0]} {lit['date']}"

        # todo: split description to more separate fields
        description = f"""{lit.get('autor') + ',' or ''} 
                    {lit.get('title') or ''} 
                    {'. In: ' + lit.get('publication') + ',' or ''} """
        print(description)

        list_.append({
            'id': lit['id'],
            'name': name,
            'type_ids': '5' if not lit.get('publication') else '4',

        })
    return list_


if __name__ == "__main__":
    data = get_data()
    literature_csv = get_literature_csv(data['literature'])
    # print(json.dumps(data, ensure_ascii=False).encode('utf8'))
    # print(literature_csv)
