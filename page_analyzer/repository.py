from psycopg2.extras import RealDictCursor


class DataBase:
    def __init__(self, conn):
        self.conn = conn

    def initialize_database(self):
        with self.conn.cursor() as cur:
            with open("database.sql", "r") as sql_file:
                sql_script = sql_file.read()
                for command in sql_script.split(";"):
                    if command.strip():
                        cur.execute(command)
            self.conn.commit()

    def add(self, url):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO urls (name) VALUES (%s) RETURNING id", (url,)
            )
            id = cur.fetchone()["id"]
            self.conn.commit()
        return id

    def get(self, id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id=%s", (id,))
            url = cur.fetchone()
        return url

    def get_by_url(self, url_name):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE name=%s", (url_name,))
            url = cur.fetchone()
        return url

    def get_content(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM urls ORDER BY created_at DESC")
            urls = cur.fetchall()
        return urls

    def add_check(
        self, url_id, status_code, h1, title, description, created_at
    ):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO url_checks (
                    url_id,
                    status_code,
                    h1, title,
                    description,
                    created_at)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (url_id, status_code, h1, title, description, created_at),
            )
            self.conn.commit()

    def get_checks_by_url_id(self, url_id):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
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
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
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
