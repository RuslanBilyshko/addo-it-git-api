import cmd

from argparser import ArgParser
from repos.repository import Repository, Commit


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

    def do_test(self, line): pass

    def do_stat(self, line):
        """Статиcтика репозитория Нужно будет указать Имя пользователя и Репозитория"""

        # """Статиcтика репозитория введите например: stat -u RuslanBilyshko -r add-it-task2.2"""

        # stat -u RuslanBilyshko -r add-it-task2.2
        # stat -u nesterenko-d -r rest-generator

        # args = ArgParser.repos(line)
        # rep = args["repos"]
        # user = args["username"]

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

    def default(self, line):
        print("Несуществующая команда")


if __name__ == "__main__":
    cli = Cli()
    try:
        cli.cmdloop()

    except KeyboardInterrupt:
        print("завершение сеанса...")
