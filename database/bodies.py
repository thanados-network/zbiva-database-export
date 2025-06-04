from config import get_cursor
from model.bodies import Body


def get_bodies_from_database() -> list[Body]:
    query = """
            SELECT id,
                   datum_vnosa           AS entry_date,
                   datum_spremembe       AS modification_date,
                   vnesel                AS entered_by,
                   najprej               AS earliest,
                   najkasneje            AS latest,
                   dolocevalec           AS author,
                   ST_AsText(koordinate) as coordinates,
                   star_id               AS star_id,
                   oznaka                AS label,
                   najmanjsa_starost     AS min_age,
                   najvecja_starost      AS max_age,
                   opombe                AS notes,
                   grob_id               AS grave_id,
                   lega_desne_roke_id    AS right_hand_position_id,
                   lega_glave_id         AS head_position_id,
                   lega_leve_roke_id     AS left_hand_position_id,
                   lega_nog_id           AS legs_position_id,
                   lega_telesa_id        AS body_position_id,
                   posebnosti_id         AS special_features_id,
                   pridatki_id           AS additions_id,
                   spol_id               AS gender_id
            FROM public.telesa_telo; \


            """
    with get_cursor() as cursor:
        cursor.execute(query)
        bodies = [Body(dict(row)) for row in cursor.fetchall()]
    return bodies
