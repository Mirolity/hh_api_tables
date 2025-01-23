import requests


class APIHandler:
    BASE_URL = "https://api.hh.ru"

    def get_employers(self, employer_ids: list) -> list:
        """
        Получает информацию о работодателях по их идентификаторам.

        :param employer_ids: Список идентификаторов работодателей.
        :return: Список работодателей.
        """
        employers = []
        for employer_id in employer_ids:
            response = requests.get(f"{self.BASE_URL}/employers/{employer_id}")
            if response.status_code == 200:
                employers.append(response.json())
        return employers

    def get_vacancies(self, employer_id: int) -> list:
        """
        Получает вакансии для указанного работодателя.

        :param employer_id: Идентификатор работодателя.
        :return: Список вакансий.
        """
        response = requests.get(f"{self.BASE_URL}/vacancies?employer_id={employer_id}")
        if response.status_code == 200:
            return response.json()['items']
        return []
