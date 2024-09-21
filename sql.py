from typing import Any

from globals import TYPE_TABLES
from literature import Literature
from place import Place


def get_places(cursor: Any) -> list[Any]:
    query = """
        SELECT 
            id,
            najprej as begin, 
            najkasneje as end,
            ime as name,
            naselje as admin_settlement,
            topografska_enota as admin_unit,
            topografsko_podrocje as admin_district,
            dezela as admin_state,
            drzava as admin_state,
            leto_prve_objave as first_publication,
            natancnost_lokacije as location_precision,
            koordinate as coordinate,
            opis_lokacije as location_description,
            parcelna_stevilka as plot_number,
            kakovost_podatkov as data_quality,
            zanesljivost_podatkov as archeologial_quality,
            posebne_najdbe as special_finds,
            opombe as comments,
            vir_datacije as primary_chronology,
            zanesljivost_datacije as certainty_of_chronology,
            datacija_opisno as chronology_desription,
            opis_najdisca as description,
            razno as description_2,
            povzetek as summary,
            primarna_kategorija_id as primary_type_id
        FROM public.najdisca_najdisce 
        ORDER BY id ASC 
            """
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [Place(dict(zip(columns, row))) for row in cursor.fetchall()]

def get_literature(cursor: Any) -> list[Literature]:
    query = """
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
    return [Literature(dict(zip(columns, row))) for row in cursor.fetchall()]


def get_types(cursor: Any) -> dict[str, list[dict[str, str]]]:
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
