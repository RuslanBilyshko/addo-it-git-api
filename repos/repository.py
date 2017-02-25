import requests
from repos.lang.trans import trans
import json

"""
Класс для работы с данными репозиториев пользователя
Работает по принципу цепных вызовов методов
что дает определенное удобство в построении запросов
Пример:
    repo = Repository('username')
    ---------------------------------------------
    - Загрузить все репозитории пользователя
        repo.all().get()
    - Выборка полей:
        repo.all().select(['field1, ...'field_n']).get()
    - Загрузить информацию о конкретном репозитории:
        repo.find('repos_name').first()
"""


class Repository:
    _base_url = "https://api.github.com/"

    def __init__(self, username: str):
        self.username = username
        self.url = self._base_url + "users/" + self.username + "/repos"
        self._collection = []

    def __getattr__(self, item):
        return self._collection[0].get(item)

    def find(self, repository: str):
        """Поиск конкретного репозитория из коллекции. Изменяет коллекцию оставляя найденый репозиторий"""
        self.url = self._base_url + "repos/" + self.username + "/" + repository
        self.all()
        self._collection = [self._collection]

        for r in self._collection:
            if repository == r.get("name"):
                self._collection = [r]
        return self

    def select(self, fields: list):
        """Выборка определенных полей из репозитория. Изменяет коллекцию оставляя только отфильтрованые данные"""

        result = []

        for repos in self._collection:

            f = {}

            for field in fields:
                f.update({field: repos.get(field)})

            result.append(f)

        self._collection = result
        return self

    def get(self) -> list:
        """Возвращает коллекцию. Рекомендуеться вызывать после всех выборок"""

        return self._collection

    def count(self):
        """Подсчитывает колличество элементов в коллекции"""

        return len(self._collection)

    def first(self):
        """Возвращает первый элемент коллекции"""

        return self._collection[0]

    def all(self):
        """Загружает полный список в коллекцию"""

        self._collection = requests.get(self.url).json()
        # from repos_data import repos_data
        # self._collection = repos_data

        return self

    def create(self, **request) -> int:
        """Создание репозитория"""

        repo = request["name"]
        secret = request["secret"]

        url = "https://api.github.com/user/repos"

        data = {
            "name": repo,
            "description": "Testting a creating repository " + repo,
            "auto_init": True,
        }

        response_create = requests.post(url, data=json.dumps(data), auth=(self.username, secret))
        status = response_create.headers.get("status")

        if status == "201 Created":
            return 201

        if status == "401 Unauthorized":
            return 401

        if status == "422 Unprocessable Entity":
            return 422

    def __str__(self):
        """Строковое представление репозиториев"""

        result = ""
        for repos in self._collection:
            for key, value in repos.items():
                result += "{}: {}\n".format(trans(key), value)

            result += "---------------------------------\n"

        return result


"""
Класс расширяющий Repository
для работы с коммитами
"""


class Commit(Repository):
    def __init__(self, repository: str, username: str):
        Repository.__init__(self, username)
        self.repository = repository
        self.url = self._base_url + "repos/" + self.username + "/" + self.repository + "/commits"


"""
Класс для работы с данными пользователя
"""


class Owner(Repository):
    def __init__(self, username):
        Repository.__init__(self, username)

        # from repos_data import repos_data
        # self._collection = [repos_data[0].get("owner")]

        self._collection = [requests.get(self.url).json()[0].get("owner")]

    def all(self): pass
