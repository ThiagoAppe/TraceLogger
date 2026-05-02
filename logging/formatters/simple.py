import logging


class SimpleFormatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )