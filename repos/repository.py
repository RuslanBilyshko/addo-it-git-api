import requests


class Repository:
    __base_url = "https://api.github.com/"

    def __init__(self, username: str):
        self.username = username
        self._collection = []

    def find(self, repository: str):
        self.all()

        for r in self._collection:
            if repository == r.get("name"):
                self._collection = [r]
        return self

    def select(self, fields: list):
        result = []

        for repos in self._collection:

            f = {}

            for field in fields:
                f.update({field: repos.get(field)})

            result.append(f)

        self._collection = result
        return self

    def get(self) -> list:
        return self._collection

    def count(self):
        return len(self._collection)

    def first(self):
        return self._collection[0]

    def all(self):
        # repo = self.__base_url + "users/" + self.username + "/repos"
        # self._collection = requests.get(repo).json()

        from repos_data import repos_data
        self._collection = repos_data
        return self

    def __str__(self):
        result = ""
        for repos in self._collection:
            for key, value in repos.items():
                result += "{}: {}\n".format(key, value)

            result += "------------------------\n"

        return result



class Commit(Repository):

    def __init__(self, repository: str, username: str):
        self.repository = repository
        Repository.__init__(self, username)


    def all(self):
        repo = self.__base_url + "users/" + self.username + "/repos"
        self._collection = requests.get(repo).json()

        # from repos_data import repos_data
        # self._collection = repos_data
        return self