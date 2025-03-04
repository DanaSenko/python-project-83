from psycopg2.extras import NamedTupleCursor
from flask import g
import psycopg2


def get_db(db_url):
    if 'db' not in g:
        g.db = psycopg2.connect(db_url)
    return g.db


def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


class DataBase:
    def __init__(self, conn):
        self.conn = conn

    def commit(self):
        self.conn.commit()

    def add_url(self, url):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                "INSERT INTO urls (name) VALUES (%s) RETURNING id", (url,)
            )
            id = cur.fetchone().id
        self.commit()
        return id

    def get_url_by_id(self, id):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id=%s", (id,))
            return cur.fetchone()

    def get_by_url(self, url_name):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE name=%s", (url_name,))
            return cur.fetchone()

    def add_check_of_url(
        self, url_id, status_code, h1, title, description, created_at
    ):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                """
                INSERT INTO url_checks (
                    url_id,
                    status_code,
                    h1, title,
                    description,
                    created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id""",
                (url_id, status_code, h1, title, description, created_at),
            )
            id = cur.fetchone().id
        self.commit()
        return id

    def get_checks_by_url_id(self, url_id):
        try:
            with self.conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(
                    """SELECT * FROM url_checks WHERE url_id=%s
                    ORDER BY id DESC""",
                    (url_id,),
                )
                return cur.fetchall()
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return []

    def get_all_urls_with_last_check(self):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                """
            SELECT
                urls.id,
                urls.name,
                urls.created_at,
                last_check.created_at AS last_check,
                last_check.status_code
            FROM urls
            LEFT JOIN (
                SELECT
                    url_id,
                    MAX(created_at) AS created_at,
                    status_code
                FROM url_checks
                GROUP BY url_id, status_code
            ) AS last_check ON urls.id = last_check.url_id
            ORDER BY urls.id DESC;
            """
            )
            urls = cur.fetchall()
        return urls
