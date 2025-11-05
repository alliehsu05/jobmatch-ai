import logging
import os


class LoggerManager:
    def __init__(self, log_file="system.log", log_dir="logs", level=logging.INFO):
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, log_file)


        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d | %(message)s",
            handlers=[
                logging.FileHandler(log_path, mode="a", encoding="utf-8")
            ]
        )

        self.logger = logging.getLogger(__name__)
        self.log_path = log_path

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg, raise_exception=False, exception_type=RuntimeError):
        self.logger.error(msg)
        if raise_exception:
            raise exception_type(msg)

logger_manager = LoggerManager()
