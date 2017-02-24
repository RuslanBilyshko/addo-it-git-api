import cmd

from repository import Repository
from argparser import ArgParser


class Cli(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.intro = "Добро пожаловать\nДля справки наберите 'help'"
        self.doc_header = "Доступные команды (для справки по конкретной команде наберите 'help _команда_')"

    def do_repo(self, line: str):
        """Получение списка репозиториев пользователя <repo -u [user_name]>"""

        # repo -u RuslanBilyshko
        # test -u nesterenko-d
        username = ArgParser.username(line)
        repo = Repository(username)
        #concrete_repository = repo.get("add-it-task2.2")

        print('Список репозиториев - ' + username)
        print("------------------------------------")



        print(repo.all())

        # for field, value in concrete_repository.items():
        #     print("{} : {}".format(field, value))
        # for name in repo.get('name'):
        #     print("repo: " + name)


    def do_stat(self, username: str, repos: str):
        pass

    def default(self, line):
        print("Несуществующая команда")


if __name__ == "__main__":
    cli = Cli()
    try:
        cli.cmdloop()

    except KeyboardInterrupt:
        print("завершение сеанса...")
