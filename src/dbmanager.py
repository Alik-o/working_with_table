import psycopg2


class DBManager:
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
        self.conn = psycopg2.connect(
            dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port
        )
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""

        self.cur.execute(
            """SELECT companies.name, COUNT(vacancies.id)
        FROM companies
        JOIN vacancies ON companies.id = vacancies.company_id
        GROUP BY companies.name;"""
        )
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты, ссылки"""

        self.cur.execute(
            """SELECT companies.name, vacancies.name,
        vacancies.salary_min, vacancies.salary_max, vacancies.url
        FROM companies
        JOIN vacancies ON companies.id = vacancies.company_id;"""
        )

        return self.cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""

        self.cur.execute(
            """
        SELECT (AVG(salary_min + salary_max)/2):: int
        FROM vacancies;"""
        )

        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""

        self.cur.execute(
            """SELECT * FROM vacancies
        WHERE salary_min > (SELECT AVG(salary_min) FROM vacancies);"""
        )

        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные ключевые слова"""

        self.cur.execute(
            f"""SELECT * FROM vacancies
        WHERE name ILIKE '%{keyword}%';"""
        )

        return self.cur.fetchall()
