import cmd
import csv
from os import path
from argparser import ArgParser
from repos.repository import Repository, Commit, Owner
from getpass import getpass
import xlwt

path_to_files = "resource/files/"


class Cli(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.intro = "Добро пожаловать\nДля справки наберите 'help'"
        self.doc_header = "Доступные команды (для справки по конкретной команде наберите 'help _команда_')"

    def do_repo(self, line: str):
        """Получение списка репозиториев пользователя. Нужно будет указать Имя пользователя"""

        # """Получение списка репозиториев пользователя введите например: repo -u RuslanBilyshko"""
        # repo -u RuslanBilyshko
        # repo -u nesterenko-d

        # username = ArgParser.username(line)
        username = input("Укажите имя пользователя: ")

        repos = Repository(username).all().select(["name"])

        print('Список репозиториев - {} ({})'.format(username, repos.count()))
        print("------------------------------------")
        print(repos)

    def do_test(self, line):
        owner = Owner('RuslanBilyshko')
        print(owner.id)

    def do_stat(self, line):
        """Статиcтика репозитория Нужно будет указать Имя пользователя и Репозитория"""

        user = input("Укажите имя пользователя: ")
        rep = input("Укажите имя репозитория: ")

        commits_count = Commit(rep, user).all().count()

        fields = [
            "id",
            "name",
            "full_name",
            "html_url",
            "language",
            "default_branch"
        ]

        repos = Repository(user).find(rep).select(fields)

        print('Статистика репозитория - /{}/ (пользователь: {})'.format(rep, user))
        print("------------------------------------")
        print("Коммитов: {}".format(commits_count))

        # При таком варианте распечатки порядок полей конечно всегда разный
        # Но ничего не стоит воспользоваться repos.get()
        # И вывести сдесь все поля в нужном порядке
        print(repos)

    def do_create(self, line):
        """Создание репозитория"""

        name = ArgParser.name(line)

        user = input("Имя пользователя: ")
        secret = getpass("Пароль: ")

        repo = Repository(user)
        status = repo.create(name=name, secret=secret)

        if status == 201:
            html_url = repo.find(name).html_url
            print("Поздравляем. Репозиторий \"{}\" успешно создан".format(name))
            print("Ссылка на репозиторий: {}".format(html_url))

        if status == 401:
            print("Ошибка авторизации")

        if status == 422:
            print("Репозиторий с таким названием уже существует.")

    def do_export(self, line):

        user = input("Имя пользователя: ")
        repository = input("Название репозитория: ")
        ext = input("Формат файла (csv / xls): ")

        fields = [
            "id",
            "name",
            "full_name",
            "html_url",
            "language",
            "default_branch"
        ]

        repo = Repository(user).find(repository).select(fields)
        path_to_file = path.abspath(path_to_files)
        res = repo.export(ext, path_to_file)

        if res:
            print("Файл успешно создан")
            print("Путь к файлу: {}/{}.{}".format(path_to_file, repo.name, ext))
        else:
            print("Ошибка экспорта. Повторите попытку")

    def default(self, line):
        print("Несуществующая команда")


if __name__ == "__main__":
    cli = Cli()
    try:
        cli.cmdloop()

    except KeyboardInterrupt:
        print("завершение сеанса...")
