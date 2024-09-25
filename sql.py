from contextlib import contextmanager

import psycopg2

from Citation import Citation
from globals import TYPE_TABLES
from literature import Literature
from place import Place


@contextmanager
def get_cursor():
    connection = psycopg2.connect(
        dbname="zbiva",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432")
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()


def get_places() -> list[Place]:
    query = """
            SELECT 
                id as id,
                najprej as begin, 
                najkasneje as "end",
                ime as name,
                naselje as admin_settlement,
                topografska_enota as admin_unit,
                topografsko_podrocje as admin_district,
                dezela as admin_state,
                drzava as admin_state2,
                leto_prve_objave as first_publication,
                natancnost_lokacije as location_precision,
                koordinate as coordinate,
                opis_lokacije as location_description,
                parcelna_stevilka as plot_number,
                kakovost_podatkov as data_quality,
                zanesljivost_podatkov as archaeological_quality,
                posebne_najdbe as special_finds,
                opombe as comments,
                vir_datacije as primary_chronology,
                zanesljivost_datacije as certainty_of_chronology,
                datacija_opisno as chronology_description,
                opis_najdisca as description,
                razno as description_2,
                povzetek as summary,
                primarna_kategorija_id as primary_type_id
            FROM public.najdisca_najdisce 
            """
    with get_cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        places = [Place(dict(zip(columns, row))) for row in cursor.fetchall()]
    return places


# todo: Get only the literature we need for sites
def get_literature() -> list[Literature]:
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
    with get_cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        lit = [Literature(dict(zip(columns, row))) for row in
               cursor.fetchall()]
    return lit


def get_citation() -> list[Citation]:
    query = """
            SELECT
                id, 
                citat AS pages,
                opomba AS description, 
                clanek_id AS literature_id,
                najdisce_id AS place_id
            FROM public.najdisca_najdisceliteratura
            """
    with get_cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        cit = [Citation(dict(zip(columns, row))) for row in cursor.fetchall()]
    return cit


def get_types() -> dict[str, list[dict[str, str]]]:
    types = {}
    for table in TYPE_TABLES:
        query = f"""
                SELECT koda, opis
                FROM public.{table};
            """
        with get_cursor() as cursor:
            cursor.execute(query)
            types[table.replace('lastnosti_najdisc_', '')] = [
                {'koda': a[0], 'opis': a[1]} for a in cursor.fetchall()]
    return types
