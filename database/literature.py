from config import get_cursor
from model.literature import Literature


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
