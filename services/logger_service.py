import logging

DEFAULT_FORMATTER = '%(levelname)s - %(asctime)s - %(message)s'
DEFAULT_FORMATTER_DATE_FMT = '%Y-%m-%d - %H:%M:%S'

DEFAULT_FILE_HANDLER = 'errors.log'


class LoggerService:
    """
    Provide methods to manage logger
    """

    def __init__(self, name, formatter=DEFAULT_FORMATTER, datefmt=DEFAULT_FORMATTER_DATE_FMT, file_handler=DEFAULT_FILE_HANDLER):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        self.formatter = logging.Formatter(formatter)
        self.formatter.datefmt = datefmt

        self.file_handler = logging.FileHandler(file_handler)
        self.file_handler.setFormatter(self.formatter)
        self.file_handler.setLevel(logging.ERROR)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.formatter)
        self.stream_handler.setLevel(logging.INFO)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

    def get_logger(self):
        """
        Get logger

        :return: void
        """
        return self.logger
