from typing import Any

from globals import TYPE_TABLES
from literature import Literature


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
