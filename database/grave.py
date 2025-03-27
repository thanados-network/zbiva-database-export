from collections import defaultdict
from typing import Any

from config import get_cursor
from globals import GRAVE_TYPE_TABLES
from model.citation import Citation
from model.grave import Grave


def get_graves_from_database() -> list[Grave]:
    query = """
        SELECT 
            g.id,
            g.datum_vnosa AS entry_date,
            g.datum_spremembe AS modification_date,
            g.vnesel AS entered_by,
            g.najprej AS earliest,
            g.najkasneje AS latest,
            g.dolocevalec AS author,
            ST_AsText(g.koordinate) as coordinates,
            g.oznaka AS grave_label,
            g.stevilo_pokojnih AS number_of_deceased,
            g.dolzina_groba AS grave_length,
            g.sirina_groba AS grave_width,
            g.globina_od AS depth_from,
            g.globina_do AS depth_to,
            g.odklon_od_severa AS deviation_from_north,
            g.odklon_opisno AS deviation_description,
            g.dolzina_krste AS coffin_length,
            g.sirina_krste AS coffin_width,
            g.opombe AS notes,
            g.najdisce_id AS site_id,
            g.vrsta_id AS type_id,
            COALESCE(ARRAY_AGG(DISTINCT ggg.gradba_id) FILTER (WHERE ggg.gradba_id IS NOT NULL), '{}') ||
            COALESCE(ARRAY_AGG(DISTINCT ggz.zasutje_id) FILTER (WHERE ggz.zasutje_id IS NOT NULL), '{}') ||
            COALESCE(ARRAY_AGG(DISTINCT ggzz.zunanjiznaki_id) FILTER (WHERE ggzz.zunanjiznaki_id IS NOT NULL), '{}') 
            AS grave_types
        FROM public.grobovi_grob g 
        LEFT JOIN public.grobovi_grob_gradba ggg on g.id = ggg.grob_id 
        LEFT JOIN public.grobovi_grob_zasutje ggz on g.id = ggz.grob_id
        LEFT JOIN public.grobovi_grob_zunanji_znaki ggzz on g.id = ggzz.grob_id
        GROUP BY g.id, g.datum_vnosa, g.datum_spremembe, g.vnesel, g.najprej,
                 g.najkasneje, g.dolocevalec, g.koordinate, g.oznaka, 
                 g.stevilo_pokojnih, g.dolzina_groba, g.sirina_groba, g.globina_od, 
                 g.globina_do, g.odklon_od_severa, g.odklon_opisno, g.dolzina_krste, 
                 g.sirina_krste, g.opombe, g.najdisce_id, g.vrsta_id;
        """
    with get_cursor() as cursor:
        cursor.execute(query)
        graves = [Grave(dict(row)) for row in cursor.fetchall()]
    return graves


def get_grave_citation_from_database() -> list[Citation]:
    query = """
            SELECT
                id, 
                citat AS pages,
                grob_id as linked_id,
                clanek_id AS literature_id,
                citat as citation
            FROM public.grobovi_grobliteratura
            """
    with get_cursor() as cursor:
        cursor.execute(query)
        cit = [Citation(dict(row)) for row in cursor.fetchall()]
    return cit


def get_grave_type_from_database() -> dict[str, dict[str, str]]:
    types: defaultdict[Any, dict[str, str]] = defaultdict(dict)
    for table in GRAVE_TYPE_TABLES:
        query = f"""
                SELECT koda, opis
                FROM public.{table};
            """
        with get_cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                types[table.replace('lastnosti_grobov_', '')][row['koda']] = \
                    row['opis']
    return types
