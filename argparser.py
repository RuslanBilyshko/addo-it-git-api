import argparse

class ArgParser(object):

    @staticmethod
    def username(line: str):
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--username', required=True)
        return parser.parse_args(line.split()).username