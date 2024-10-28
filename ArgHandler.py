import argparse


class ArgHandler:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="The Nightman Scanneth - A simple Python port scanner."
        )
        self.__create_args()

    def get_options(self) -> dict:
        self.args = self.parser.parse_args()
        return self.args

    def __create_args(self) -> None:
        self.parser.add_argument(
            "--host",
            default="127.0.0.1",
            help="The host to port scan against. Default [127.0.0.1]",
        )
        self.parser.add_argument(
            "--ports",
            "-p",
            type=str,
            default="1-100",
            help="The ports to scan. Can be a range. Default [1-100]",
        )
        self.parser.add_argument(
            "--concurrent",
            "-c",
            type=int,
            default=50,
            help="The max number of concurrent network requests. Default [50]",
        )
