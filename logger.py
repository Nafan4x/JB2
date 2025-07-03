import logging


class CustomLogger:
    def __init__(
        self,
        name: str,
        log_file: str,
        console_level=logging.WARNING,
        file_level=logging.DEBUG,
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # общий уровень логгера — самый низкий

        if not self.logger.hasHandlers():
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

            # Консольный хендлер
            ch = logging.StreamHandler()
            ch.setLevel(console_level)  # уровень для консоли
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

            # Файловый хендлер
            fh = logging.FileHandler(f"logging\{log_file}", encoding="utf-8")
            fh.setLevel(file_level)  # уровень для файла
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger
