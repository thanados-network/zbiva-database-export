from contextlib import contextmanager
from typing import Any, Generator

import psycopg2
from psycopg2 import extras


@contextmanager
def get_cursor() -> Generator[Any, None, None]:
    connection = psycopg2.connect(
        dbname="zbiva",
        user="openatlas",
        password="openatlas",
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
