import psycopg2
from psycopg2 import sql


class DBManager:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        """
        Инициализация подключения к базе данных.

        :param dbname: Имя базы данных.
        :param user: Имя пользователя.
        :param password: Пароль.
        :param host: Хост.
        :param port: Порт.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = self._connect_to_db()

    def _connect_to_db(self):
        """
        Подключается к базе данных. Если база данных не существует, создает её.
        """
        try:
            connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            connection.autocommit = True
            return connection
        except psycopg2.OperationalError:
            # Если база данных не существует, создаем её
            connection = psycopg2.connect(
                dbname="postgres",  # Подключаемся к стандартной базе данных
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {self.dbname}")
            connection.close()
            return self._connect_to_db()  # Повторно подключаемся к новой базе данных

    def create_tables(self):
        """
        Создает таблицы employers и vacancies.
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    employer_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    url VARCHAR(255)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(employer_id),
                    title VARCHAR(255) NOT NULL,
                    salary INTEGER,
                    url VARCHAR(255)
                )
            """)

    def insert_employers(self, employers: list):
        """
        Вставляет данные о работодателях в таблицу employers.

        :param employers: Список работодателей.
        """
        with self.connection.cursor() as cursor:
            for employer in employers:
                cursor.execute("""
                    INSERT INTO employers (employer_id, name, url)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (employer_id) DO NOTHING
                """, (employer['id'], employer['name'], employer['alternate_url']))

    def insert_vacancies(self, vacancies: list):
        """
        Вставляет данные о вакансиях в таблицу vacancies.

        :param vacancies: Список вакансий.
        """
        with self.connection.cursor() as cursor:
            for vacancy in vacancies:
                cursor.execute("""
                    INSERT INTO vacancies (vacancy_id, employer_id, title, salary, url)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO NOTHING
                """, (vacancy['id'], vacancy['employer']['id'], vacancy['name'], vacancy.get('salary', {}).get('from'), vacancy['alternate_url']))

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.

        :return: Список компаний и количество вакансий.
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, COUNT(v.vacancy_id)
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.name
            """)
            return cursor.fetchall()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.

        :return: Список всех вакансий.
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, v.title, v.salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
            """)
            return cursor.fetchall()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.

        :return: Средняя зарплата.
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT AVG(salary)
                FROM vacancies
                WHERE salary IS NOT NULL
            """)
            return cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

        :return: Список вакансий с зарплатой выше средней.
        """
        avg_salary = self.get_avg_salary()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, v.title, v.salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE v.salary > %s
            """, (avg_salary,))
            return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.

        :param keyword: Ключевое слово для поиска.
        :return: Список вакансий, содержащих ключевое слово.
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, v.title, v.salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE v.title ILIKE %s
            """, (f"%{keyword}%",))
            return cursor.fetchall()
