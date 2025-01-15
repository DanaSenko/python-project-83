from psycopg2.extras import RealDictCursor


class DataBase:
    def __init__(self, conn):
        self.conn = conn

    
    def initialize_database(self):
        with self.conn.cursor() as cur:
            with open('database.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            # Выполняем SQL-скрипт
            cur.execute(sql_script)
            self.conn.commit()


    def add(self, url):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("INSERT INTO urls (name) VALUES (%s) RETURNING id", (url,))
            url_id = cur.fetchone()
            self.conn.commit()
        return url

    def get(self, id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id=%s", (id,))
            url = cur.fetchone()
            self.conn.commit()
        return url

    def get_by_url(self, url_name):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE name=%s", (url_name,))
            url = cur.fetchone()
        return url


    def get_content(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM urls ORDER BY created_at DESC")
            urls = cur.fetchall()
        return urls

    def add_chek(self, url_id, status_code, h1, title, description, created_at):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO url_cheks (url_id, status_code, h1, title, description, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (url_id, status_code, h1, title, description, created_at),
            )

    def get_checks_by_url_id(self, url_id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            try:
                with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(
                        "SELECT id, created_at FROM url_checks WHERE url_id=%s ORDER BY created_at DESC",
                        (url_id,))
                    checks = cur.fetchall()
                return checks
            except Exception as e:
                self.conn.rollback()
                print(f"Ошибка при выполнении запроса: {e}")

    """
    Выведите в списке сайтов дату последней проверки рядом с каждым сайтом
    """

    def get_all_urls_with_last_check(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    urls.id, 
                    urls.name, 
                    urls.created_at, 
                    MAX(url_checks.created_at) AS last_check
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                GROUP BY urls.id
                ORDER BY urls.created_at DESC;
            """)
            urls = cur.fetchall()
        return urls
