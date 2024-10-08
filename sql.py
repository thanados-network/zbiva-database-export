from collections import defaultdict
from contextlib import contextmanager
from typing import Any, Generator

import psycopg2
from psycopg2 import extras

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
    cursor: Any = connection.cursor(cursor_factory=extras.RealDictCursor)
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
            n.id as id,
            n.najprej as begin, 
            n.najkasneje as "end",
            n.ime as name,
            n.naselje as admin_settlement,
            n.topografska_enota as admin_unit,
            n.topografsko_podrocje as admin_district,
            n.dezela as admin_state,
            n.drzava as admin_state2,
            n.leto_prve_objave as first_publication,
            n.natancnost_lokacije as location_precision,
            n.koordinate as coordinate,
            n.opis_lokacije as location_description,
            n.parcelna_stevilka as plot_number,
            n.kakovost_podatkov as data_quality,
            n.zanesljivost_podatkov as archaeological_quality,
            n.posebne_najdbe as special_finds,
            n.opombe as comments,
            n.vir_datacije as primary_chronology,
            n.dolocevalec as author_of_site,
            n.zanesljivost_datacije as certainty_of_chronology,
            n.datacija_opisno as chronology_description,
            n.opis_najdisca as description,
            n.razno as description_2,
            n.povzetek as summary,
            n.primarna_kategorija_id as primary_type_id,
            
            ARRAY_REMOVE(
                ARRAY_CAT(
                    ARRAY[
                        zak.obmocje_id,
                        nasel.tip_id,
                        nasel.utrjenost_id,
                        nasel.velikost_id,
                        nasel.vrste_sledov_id,
                        kult.tip_id,
                        grob.nacin_pokopa_id,
                        grob.oddaljenost_id,
                        grob.prostor_id,
                        grob.tip_id,
                        grob.usmerjenost_pobocja_id,
                        grob.velikost_id
                    ],
                    ARRAY_CAT(
                        ARRAY_AGG(DISTINCT topo.topografskalega_id),
                        ARRAY_AGG(DISTINCT najbe.najdba_id)
                    )
                ), NULL
            ) AS site_types
        FROM public.najdisca_najdisce n
        LEFT JOIN public.najdisca_zakladnanajdba zak ON zak.najdisce_id = n.id
        LEFT JOIN public.najdisca_naselbina nasel ON nasel.najdisce_id = n.id
        LEFT JOIN public.najdisca_najdisce_topografske_lege topo ON topo.najdisce_id = n.id
        LEFT JOIN public.najdisca_najdisce_najdbe najbe ON najbe.najdisce_id = n.id
        LEFT JOIN public.najdisca_kultniprostor kult ON kult.najdisce_id = n.id
        LEFT JOIN public.najdisca_grobisce grob ON grob.najdisce_id = n.id
        GROUP BY n.id, zak.obmocje_id, nasel.tip_id, nasel.utrjenost_id, 
        nasel.velikost_id, nasel.vrste_sledov_id, kult.tip_id, 
        grob.nacin_pokopa_id, grob.oddaljenost_id, grob.prostor_id, 
        grob.tip_id, grob.usmerjenost_pobocja_id, grob.velikost_id;
        """
    with get_cursor() as cursor:
        cursor.execute(query)
        places = [Place(dict(row)) for row in cursor.fetchall()]
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
        lit = [Literature(dict(row)) for row in cursor.fetchall()]
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
        cit = [Citation(dict(row)) for row in cursor.fetchall()]
    return cit


def get_type_names_from_database() -> dict[str, dict[str, str]]:
    types: defaultdict[Any, dict[str, str]] = defaultdict(dict)
    for table in TYPE_TABLES:
        query = f"""
                SELECT koda, opis
                FROM public.{table};
            """
        with get_cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                types[table.replace('lastnosti_najdisc_', '')][row['koda']] = \
                row['opis']
    return types











