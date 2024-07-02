import argparse
import logging
import os

import settings
import settings_logging
from controller import Controller

logger = logging.getLogger("main")


def main():
    try:
        settings_logging.setup_logger(settings.LOG_LEVEL)

        parser = argparse.ArgumentParser(description="AI Helper Command Line Interface")
        parser.add_argument(
            "-w", "--work-dir", type=str, help="Working directory for the assistant"
        )

        args = parser.parse_args()

        if not settings.AGENT_WORK_DIR:
            settings.AGENT_WORK_DIR = os.path.join(os.getcwd(), "work_dir")

        if args.work_dir:
            settings.AGENT_WORK_DIR = args.work_dir

        os.makedirs(settings.AGENT_WORK_DIR, exist_ok=True)
        logger.info(f"Using work dir: {settings.AGENT_WORK_DIR}")

        controller = Controller()
        controller.start()
    except KeyboardInterrupt:
        logger.info("Ctrl-C pressed, exiting...")


if __name__ == "__main__":
    main()
