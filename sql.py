from collections import defaultdict
from contextlib import contextmanager
from typing import Any, Generator

import psycopg2

from citation import Citation
from globals import TYPE_TABLES
from literature import Literature
from place import Place


@contextmanager
def get_cursor() -> Generator[Any, None, None]:
    connection = psycopg2.connect(
        dbname="zbiva",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432")
    cursor: Any = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()


def get_places_from_database() -> list[Place]:
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


def get_literature_from_database() -> list[Literature]:
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


def get_place_citation_from_database() -> list[Citation]:
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


def get_type_names_from_database() -> dict[str, dict[str, str]]:
    types: defaultdict[Any, dict[str, str]]= defaultdict(dict)
    for table in TYPE_TABLES:
        query = f"""
                SELECT koda, opis
                FROM public.{table};
            """
        with get_cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                types[table.replace('lastnosti_najdisc_', '')][row[0]] = row[1]
    return types


def fetch_site_grave_types() -> dict[str, list[str]]:
    types = defaultdict(list)
    query = """
        SELECT 
            najdisce_id,
            nacin_pokopa_id,
            oddaljenost_id,
            prostor_id,
            tip_id,
            usmerjenost_pobocja_id,
            velikost_id 
        FROM public.najdisca_grobisce;
        """
    with get_cursor() as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            types[row[0]] = [row[1], row[2], row[3], row[4], row[5], row[6]]
    return types


def fetch_site_cult_types() -> dict[str, list[str]]:
    types = defaultdict(list)
    query = """
        SELECT 
            najdisce_id,
            tip_id
        FROM public.najdisca_kultniprostor;
        """
    with get_cursor() as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            types[row[0]] = [row[1]]
    return types


def fetch_site_finds_types() -> dict[str, list[str]]:
    types = defaultdict(list)
    query = """
        SELECT 
            najdisce_id,
            najdba_id
        FROM public.najdisca_najdisce_najdbe;
        """
    with get_cursor() as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            types[row[0]] = [row[1]]
    return types


def fetch_site_topography_types() -> dict[str, list[str]]:
    types = defaultdict(list)
    query = """
        SELECT 
            najdisce_id,
            topografskalega_id
        FROM public.najdisca_najdisce_topografske_lege;
        """
    with get_cursor() as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            types[row[0]] = [row[1]]
    return types


def fetch_site_settlement_types() -> dict[str, list[str]]:
    types = defaultdict(list)
    query = """
        SELECT 
            najdisce_id,
            tip_id,
            utrjenost_id,
            velikost_id,
            vrste_sledov_id
        FROM public.najdisca_naselbina;
        """
    with get_cursor() as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            types[row[0]] = [row[1], row[2], row[3], row[4]]
    return types


def fetch_site_other_types() -> dict[str, list[str]]:
    types = defaultdict(list)
    query = """
        SELECT 
            najdisce_id
        FROM public.najdisca_ostalo;
        """
    with get_cursor() as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            types[row[0]] = ['OTHER']
    return types


def fetch_site_depot_types() -> dict[str, list[str]]:
    types = defaultdict(list)
    query = """
        SELECT 
            najdisce_id,
            obmocje_id
        FROM public.najdisca_zakladnanajdba;
        """
    with get_cursor() as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            types[row[0]] = [row[1]]
    return types
