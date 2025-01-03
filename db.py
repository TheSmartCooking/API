from contextlib import contextmanager

import pymysql.cursors
from flask import current_app


def get_db_connection():
    return pymysql.connect(
        host=current_app.config["MYSQL_HOST"],
        user=current_app.config["MYSQL_USER"],
        password=current_app.config["MYSQL_PASSWORD"],
        database=current_app.config["MYSQL_DB"],
        cursorclass=pymysql.cursors.DictCursor,
    )


@contextmanager
def database_cursor():
    db = get_db_connection()
    try:
        yield db.cursor()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
