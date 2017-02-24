import argparse

class ArgParser(object):

    @staticmethod
    def username(line: str) -> str:
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--username', required=True)
        return parser.parse_args(line.split()).username

    @staticmethod
    def repos(line: str) -> dict:
        parser = argparse.ArgumentParser()
        parser.add_argument('-r', '--repos', required=True)
        parser.add_argument('-u', '--username', required=True)
        result = parser.parse_args(line.split())
        return {"username": result.username, "repos": result.repos }