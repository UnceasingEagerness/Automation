import logging
from pathlib import Path


class AutomationLogger:
    """
    Central logger used throughout the framework.

    Usage:

        from automation.utils.logger import get_logger

        logger = get_logger("Scheduler")

        logger.info("Job queued")
    """

    _configured = False

    @classmethod
    def configure(cls):

        if cls._configured:
            return

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        root = logging.getLogger("Automation")
        root.setLevel(logging.INFO)

        #
        # Prevent duplicate handlers.
        #

        root.handlers.clear()

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(name)-18s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        #
        # Console
        #

        console = logging.StreamHandler()
        console.setFormatter(formatter)

        #
        # File
        #

        logfile = logging.FileHandler(
            log_dir / "automation.log"
        )

        logfile.setFormatter(formatter)

        root.addHandler(console)
        root.addHandler(logfile)

        cls._configured = True

    @classmethod
    def get_logger(cls, name: str):

        cls.configure()

        return logging.getLogger(f"Automation.{name}")


def get_logger(name: str):

    return AutomationLogger.get_logger(name)