from config import get_cursor
from model.citation import Citation
from model.grave import Grave


def get_graves_from_database() -> list[Grave]:
    query = """
        SELECT 
            id,
            datum_vnosa AS entry_date,
            datum_spremembe AS modification_date,
            vnesel AS entered_by,
            najprej AS earliest,
            najkasneje AS latest,
            dolocevalec AS author,
            koordinate AS coordinates,
            oznaka AS grave_label,
            stevilo_pokojnih AS number_of_deceased,
            dolzina_groba AS grave_length,
            sirina_groba AS grave_width,
            globina_od AS depth_from,
            globina_do AS depth_to,
            odklon_od_severa AS deviation_from_north,
            odklon_opisno AS deviation_description,
            dolzina_krste AS coffin_length,
            sirina_krste AS coffin_width,
            opombe AS notes,
            najdisce_id AS site_id,
            vrsta_id AS type_id
        FROM public.grobovi_grob;

        """
    with get_cursor() as cursor:
        cursor.execute(query)
        places = [Grave(dict(row)) for row in cursor.fetchall()]
    return places


def get_place_citation_from_database() -> list[Citation]:
    query = """
            SELECT
                id, 
                citat AS pages,
                opomba AS description, 
                clanek_id AS literature_id,
                najdisce_id AS place_id
            FROM ppublic.grobovi_grobliteratura
            """
    with get_cursor() as cursor:
        cursor.execute(query)
        cit = [Citation(dict(row)) for row in cursor.fetchall()]
    return cit
