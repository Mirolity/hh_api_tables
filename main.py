from api_handler import APIHandler
from db_manager import DBManager
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()


def fill_database():
    """Заполняет базу данных данными о компаниях и вакансиях."""
    api_handler = APIHandler()
    employer_ids = [1740, 2180, 3529, 3776, 906, 15478, 1724, 1934, 1939, 2310]

    # Получение данных о компаниях и вакансиях
    employers = api_handler.get_employers(employer_ids)
    vacancies = []
    for employer in employers:
        vacancies.extend(api_handler.get_vacancies(employer['id']))

    # Инициализация DBManager
    db_manager = DBManager(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

    # Создание таблиц и заполнение данных
    db_manager.create_tables()
    db_manager.insert_employers(employers)
    db_manager.insert_vacancies(vacancies)

    print("База данных успешно заполнена.")


def user_interface():
    """Интерфейс взаимодействия с пользователем."""
    db_manager = DBManager(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

    while True:
        print("\nВыберите действие:")
        print("1. Получить список всех компаний и количество вакансий у каждой компании")
        print("2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию")
        print("3. Получить среднюю зарплату по вакансиям")
        print("4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям")
        print("5. Получить список всех вакансий, в названии которых содержатся переданные в метод слова")
        print("6. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            companies = db_manager.get_companies_and_vacancies_count()
            for company in companies:
                print(f"Компания: {company[0]}, Количество вакансий: {company[1]}")

        elif choice == '2':
            vacancies = db_manager.get_all_vacancies()
            for vacancy in vacancies:
                print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")

        elif choice == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")

        elif choice == '4':
            vacancies = db_manager.get_vacancies_with_higher_salary()
            for vacancy in vacancies:
                print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")

        elif choice == '5':
            keyword = input("Введите ключевое слово: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for vacancy in vacancies:
                print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")

        elif choice == '6':
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    print("1. Заполнить базу данных")
    print("2. Запустить интерфейс пользователя")
    choice = input("Введите номер действия: ")

    if choice == '1':
        fill_database()
    elif choice == '2':
        user_interface()
    else:
        print("Неверный выбор.")
