import requests


class HeadHunterAPI:

    def __init__(self):
        self.__url_vacancies = "https://api.hh.ru/vacancies"
        self.__url_employer = f"https://api.hh.ru/employers/{'employer_id'}"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.employer_id = (1305103, 1373, 611846, 45681, 1634828, 9764865, 1947564, 37318, 697283, 2261)
        self.__params = {
            "text": "",
            "page": 0,
            "per_page": 100,
            "only_with_salary": "true",
            "employer_id": self.employer_id,
        }
        self.vacancies = []
        self.employer = []

    def get_vacancies(self):
        while self.__params.get("page") != 20:
            response = requests.get(self.__url_vacancies, headers=self.__headers, params=self.__params)
            if response.status_code != 200:
                print(f"Ошибка при запросе к API. Код ошибки: {response.status_code}")
            vacancies = response.json()["items"]
            self.vacancies.extend(vacancies)
            self.__params["page"] += 1
            if response.json()["pages"] == self.__params["page"]:
                self.__params["page"] = 0
                break

        return self.vacancies

    def get_employer(self):
        for employer_id in self.employer_id:
            self.__url_employer = f"https://api.hh.ru/employers/{employer_id}"
            response = requests.get(self.__url_employer, headers=self.__headers)
            if response.status_code == 200:
                employer = response.json()
                self.employer.append(
                    {
                        "name": employer["name"],
                        "description": employer["description"],
                        "city": employer["area"]["name"],
                    }
                )
            else:
                print(f"Ошибка при запросе к API. Код ошибки: {response.status_code}")
        return self.employer
