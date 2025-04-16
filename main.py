import logging

import agent
import settings
import settings_logging

from utils import print_and_log

logger = logging.getLogger("main")


def main():
    _agent = agent.Agent()

    running = True
    settings_logging.setup_logger(settings.LOG_LEVEL)

    logger.info(f"LLM host: {settings.LLM_HOST}")
    logger.info(f"Model: {settings.LLM_MODEL}")

    print_and_log(_agent.greeting, logger=logger)

    while running:
        try:
            user_input = input(" :").strip()
            response = _agent.respond(user_input)
            print_and_log(response, logger=logger)

        except KeyboardInterrupt:
            logger.info("Ctrl-C pressed, exiting...")
            running = False


if __name__ == "__main__":
    main()
