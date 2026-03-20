from collections import defaultdict
from typing import Any

from config import get_cursor
from globals import ARTIFACT_TYPE_TABLES
from model.artifacts import Artifact
from model.citation import Citation


def get_artifacts_from_database() -> list[Artifact]:
    query = """
            SELECT 
                p.id,
                p.datum_vnosa AS entry_date,
                p.datum_spremembe AS modification_date,
                p.vnesel AS entered_by,
                p.najprej AS earliest,
                p.najkasneje AS latest,
                p.dolocevalec AS author,
                ST_AsText(p.koordinate) AS coordinates,
                p.star_id,
                p.stratigrafska_enota AS stratigraphic_unit,
                p.interna_oznaka AS internal_label,
                p.original,
                p.stevilo_kosov AS number_of_pieces,
                p.dolzina AS length,
                p.sirina AS width,
                p.debelina AS thickness,
                p.teza AS weight,
                p.drugi_merski_podatki AS other_measurements,
                p.opombe AS notes,
                p.najdisce_id AS site_id,
                p.ohranjenost_id AS preservation_id,
                p.okolje_id AS environment_id,
                p.vrsta_id AS type_id,
                
                -- Gräber-Verknüpfung
                (SELECT STRING_AGG(CAST(grob_id AS TEXT), ', ') 
                 FROM public.predmeti_predmet_grob 
                 WHERE predmet_id = p.id) AS grave_ids,
                
                -- Boolean-Tabellen (Flag-Tabellen)
                EXISTS (SELECT 1 FROM public.predmeti_ostalo WHERE predmet_id = p.id) AS has_ostalo,
                EXISTS (SELECT 1 FROM public.predmeti_jagoda WHERE predmet_id = p.id) AS has_jagoda,
                EXISTS (SELECT 1 FROM public.predmeti_naglavniobrocek WHERE predmet_id = p.id) AS has_naglavniobrocek,
                EXISTS (SELECT 1 FROM public.predmeti_noz WHERE predmet_id = p.id) AS has_noz,
                EXISTS (SELECT 1 FROM public.predmeti_posoda WHERE predmet_id = p.id) AS has_posoda,
                EXISTS (SELECT 1 FROM public.predmeti_prstan WHERE predmet_id = p.id) AS has_prstan,
                EXISTS (SELECT 1 FROM public.predmeti_zaponka WHERE predmet_id = p.id) AS has_zaponka,
                
                -- Typisierungen & Eigenschaften (lastnosti_predmetov_*)
                (SELECT STRING_AGG(COALESCE(l.opis_de, l.opis), ', ') 
                 FROM public.predmeti_predmet_snovi c 
                 JOIN public.lastnosti_predmetov_snov l ON c.snov_id = l.koda 
                 WHERE c.predmet_id = p.id) AS material,
                (SELECT STRING_AGG(COALESCE(l.opis_de, l.opis), ', ') 
                 FROM public.predmeti_predmet_lega c 
                 JOIN public.lastnosti_predmetov_lega l ON c.lega_id = l.koda 
                 WHERE c.predmet_id = p.id) AS position,
                (SELECT STRING_AGG(COALESCE(l.opis_de, l.opis), ', ') 
                 FROM public.predmeti_jagoda_barva c 
                 JOIN public.lastnosti_predmetov_jagodabarva l ON c.jagodabarva_id = l.koda 
                 WHERE c.jagoda_id = p.id) AS bead_color,
                (SELECT STRING_AGG(COALESCE(l.opis_de, l.opis), ', ') 
                 FROM public.predmeti_jagoda_okras c 
                 JOIN public.lastnosti_predmetov_jagodaokras l ON c.jagodaokras_id = l.koda 
                 WHERE c.jagoda_id = p.id) AS bead_ornament,
                (SELECT STRING_AGG(COALESCE(l.opis_de, l.opis), ', ') 
                 FROM public.predmeti_jagoda_steklo c 
                 JOIN public.lastnosti_predmetov_jagodasteklo l ON c.jagodasteklo_id = l.koda 
                 WHERE c.jagoda_id = p.id) AS bead_glass,
                (SELECT STRING_AGG(COALESCE(l.opis_de, l.opis), ', ') 
                 FROM public.predmeti_noz_noznica c 
                 JOIN public.lastnosti_predmetov_noznoznica l ON c.noznoznica_id = l.koda 
                 WHERE c.noz_id = p.id) AS knife_sheath,
                (SELECT STRING_AGG(COALESCE(l.opis_de, l.opis), ', ') 
                 FROM public.predmeti_posoda_izdelava c 
                 JOIN public.lastnosti_predmetov_posodaizdelava l ON c.posodaizdelava_id = l.koda 
                 WHERE c.posoda_id = p.id) AS vessel_manufacture,
                (SELECT STRING_AGG(COALESCE(l.opis_de, l.opis), ', ') 
                 FROM public.predmeti_posoda_odtis c 
                 JOIN public.lastnosti_predmetov_posodaodtis l ON c.posodaodtis_id = l.koda 
                 WHERE c.posoda_id = p.id) AS vessel_impression,
                (SELECT STRING_AGG(COALESCE(l.opis_de, l.opis), ', ') 
                 FROM public.predmeti_posoda_ohranjeni_del c 
                 JOIN public.lastnosti_predmetov_posodaohranjenidel l ON c.posodaohranjenidel_id = l.koda 
                 WHERE c.posoda_id = p.id) AS vessel_preserved_part,
                (SELECT STRING_AGG(COALESCE(l.opis_de, l.opis), ', ') 
                 FROM public.predmeti_posoda_okras c 
                 JOIN public.lastnosti_predmetov_posodaokras l ON c.posodaokras_id = l.koda 
                 WHERE c.posoda_id = p.id) AS vessel_ornament,
                (SELECT STRING_AGG(COALESCE(l.opis_de, l.opis), ', ') 
                 FROM public.predmeti_posoda_vrsta_pustila c 
                 JOIN public.lastnosti_predmetov_posodavrstapustila l ON c.posodavrstapustila_id = l.koda 
                 WHERE c.posoda_id = p.id) AS vessel_temper_type
                 
            FROM public.predmeti_predmet p;
            """
    with get_cursor() as cursor:
        cursor.execute(query)
        artifacts = [Artifact(dict(row)) for row in cursor.fetchall()]
    return artifacts


def get_artifact_citation_from_database() -> list[Citation]:
    query = """
            SELECT
                id, 
                citat AS pages,
                predmet_id as linked_id,
                clanek_id AS literature_id,
                citat as citation
            FROM public.predmeti_predmetliteratura
            """
    with get_cursor() as cursor:
        cursor.execute(query)
        cit = [Citation(dict(row)) for row in cursor.fetchall()]
    return cit


def get_artifact_type_from_database() -> dict[str, dict[str, str]]:
    types: defaultdict[Any, dict[str, str]] = defaultdict(dict)
    for table in ARTIFACT_TYPE_TABLES:
        query = f"""
                SELECT koda, opis
                FROM public.{table};
            """
        with get_cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                types[
                    table.replace('lastnosti_predmetov_', '')][row['koda']] = \
                    row['opis']
    return types
