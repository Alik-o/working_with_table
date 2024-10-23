import psycopg2


class CompletionDB:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        check = self.check_database_exists()
        if not check:
            conn = psycopg2.connect(user=self.user, password=self.password, host=self.host, port=self.port)
            cursor = conn.cursor()

            cursor.execute(f"CREATE DATABASE {self.dbname}")

            conn.commit()
            cursor.close()
            conn.close()

        self.conn = psycopg2.connect(
            dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port
        )
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.conn.close()

    def check_database_exists(self):
        conn = psycopg2.connect(user=self.user, password=self.password, host=self.host, port=self.port)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.dbname,))
        exists = cursor.fetchone()

        cursor.close()
        conn.close()

        return exists is not None

    def create_table(self):
        self.cur.execute("DROP TABLE IF EXISTS vacancies CASCADE;")
        self.cur.execute("DROP TABLE IF EXISTS companies CASCADE;")
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                city TEXT NOT NULL,
                description TEXT
            )"""
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                city TEXT NOT NULL,
                company_id INTEGER REFERENCES companies(id),
                salary_min INTEGER,
                salary_max INTEGER,
                currency TEXT,
                url TEXT NOT NULL
            )"""
        )

        self.conn.commit()

    def insert_companies(self, hh_companies):
        for company in hh_companies:
            self.insert_company(company["name"], company["city"], company["description"])

    def insert_company(self, name, city, description):
        self.cur.execute(
            "INSERT INTO companies (name, city, description) VALUES (%s, %s, %s)", (name, city, description)
        )
        self.conn.commit()

    def insert_vacancies(self, hh_vacancies):
        for vacancy in hh_vacancies:
            self.insert_vacancy(
                vacancy["name"],
                vacancy["snippet"]["responsibility"],
                vacancy["area"]["name"],
                vacancy["salary"]["from"],
                vacancy["salary"]["to"],
                vacancy["salary"]["currency"],
                vacancy["alternate_url"],
                vacancy["employer"]["name"],
            )

    def insert_vacancy(self, name, description, city, salary_min, salary_max, currency, url, company):

        self.cur.execute("""SELECT id FROM companies WHERE name = %s""", (company,))
        result = self.cur.fetchone()
        company_id = result[0]

        self.cur.execute(
            """INSERT INTO vacancies
        (name, description, city, company_id, salary_min, salary_max, currency, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (name, description, city, company_id, salary_min, salary_max, currency, url),
        )
        self.conn.commit()
