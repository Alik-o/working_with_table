from config import config
from src.completiondb import CompletionDB
from src.dbmanager import DBManager
from src.head_hunter_api import HeadHunterAPI


def user_interaction():
    params = config()

    print("Ожидайте...")
    db = CompletionDB(**params)
    db.create_table()

    hh = HeadHunterAPI()

    hh_employer = hh.get_employer()
    hh_vacancies = hh.get_vacancies()

    db.insert_companies(hh_employer)
    db.insert_vacancies(hh_vacancies)
    db.disconnect()

    db_manager = DBManager(**params)
    user_input = None

    while user_input != 0:
        user_input = int(
            input(
                "1. Вывести список всех компаний и количество вакансий у каждой компании\n"
                "2. Вывести список всех вакансий\n"
                "3. Вывести среднюю зарплату по вакансиям\n"
                "4. Вывести вакансии с зарплатой выше средней по всем вакансиям\n"
                "5. Вывести вакансии с ключевым словом\n"
                "0. Выход\n"
                "Ваш выбор: "
            )
        )

        if user_input == 1:
            print(db_manager.get_companies_and_vacancies_count())
        elif user_input == 2:
            print(db_manager.get_all_vacancies())
        elif user_input == 3:
            print(db_manager.get_avg_salary())
        elif user_input == 4:
            print(db_manager.get_vacancies_with_higher_salary())
        elif user_input == 5:
            keyword = input("Введите ключевое слово: ")
            print(db_manager.get_vacancies_with_keyword(keyword))

    db_manager.disconnect()


if __name__ == "__main__":
    user_interaction()
