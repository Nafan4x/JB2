import os
import logging  # не забудьте импортировать logging, если ещё не импортирован


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

            # Убедиться, что папка для логов существует
            log_dir = "logging"
            os.makedirs(log_dir, exist_ok=True)

            # Файловый хендлер
            fh = logging.FileHandler(os.path.join(log_dir, log_file), encoding="utf-8")
            fh.setLevel(file_level)  # уровень для файла
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger
