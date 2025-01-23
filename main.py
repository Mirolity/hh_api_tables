from api_handler import APIHandler
from db_manager import DBManager


def main():
    # Инициализация APIHandler
    api_handler = APIHandler()

    # Список интересующих компаний
    employer_ids = [1740, 2180, 3529, 3776, 906, 15478, 1724, 1934, 1939, 2310]

    # Получение данных о компаниях и вакансиях
    employers = api_handler.get_employers(employer_ids)
    vacancies = []
    for employer in employers:
        vacancies.extend(api_handler.get_vacancies(employer['id']))

    # Инициализация DBManager
    db_manager = DBManager(
        dbname='your_db_name',
        user='your_db_user',
        password='your_db_password',
        host='your_db_host',
        port='your_db_port'
    )

    # Создание таблиц
    db_manager.create_tables()

    # Вставка данных в таблицы
    db_manager.insert_employers(employers)
    db_manager.insert_vacancies(vacancies)

    # Пример использования методов DBManager
    print("Компании и количество вакансий:")
    print(db_manager.get_companies_and_vacancies_count())

    print("Все вакансии:")
    print(db_manager.get_all_vacancies())

    print("Средняя зарплата:")
    print(db_manager.get_avg_salary())

    print("Вакансии с зарплатой выше средней:")
    print(db_manager.get_vacancies_with_higher_salary())

    print("Вакансии с ключевым словом 'python':")
    print(db_manager.get_vacancies_with_keyword('python'))


if __name__ == "__main__":
    main()
