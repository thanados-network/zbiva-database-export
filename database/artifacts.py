from collections import defaultdict
from typing import Any

from config import get_cursor
from globals import ARTIFACT_TYPE_TABLES
from model.artifacts import Artifact


def get_bodies_from_database() -> list[Artifact]:
    query = """
            SELECT id,
                   datum_vnosa          AS entry_date,
                   datum_spremembe      AS modification_date,
                   vnesel               AS entered_by,
                   najprej              AS earliest,
                   najkasneje           AS latest,
                   dolocevalec          AS author,
                   koordinate           AS coordinates,
                   star_id              AS star_id,
                   stratigrafska_enota  AS stratigraphic_unit,
                   interna_oznaka       AS internal_label,
                   original             AS original,
                   stevilo_kosov        AS number_of_pieces,
                   primarna_uporaba     AS primary_use,
                   dolzina              AS length,
                   sirina               AS width,
                   debelina             AS thickness,
                   teza                 AS weight,
                   drugi_merski_podatki AS other_measurements,
                   opombe               AS notes,
                   najdisce_id          AS site_id,
                   ohranjenost_id       AS preservation_id,
                   okolje_id            AS environment_id,
                   vrsta_id             AS type_id
            FROM public.predmeti_predmet; \
            """
    with get_cursor() as cursor:
        cursor.execute(query)
        artifacts = [Artifact(dict(row)) for row in cursor.fetchall()]
    return artifacts


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
