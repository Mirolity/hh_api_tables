from db_manager import DBManager


def user_interface():
    db_manager = DBManager(
        dbname='your_db_name',
        user='your_db_user',
        password='your_db_password',
        host='your_db_host',
        port='your_db_port'
    )

    while True:
        print("Выберите действие:")
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
    user_interface()
