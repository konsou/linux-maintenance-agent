import logging

from agent.agent import Agent

logger = logging.getLogger(__name__)


def chat_session():
    logger.info("AI Helper Chat Session. Type 'exit' to end the session.")
    agent = Agent(name="Alice")
    logger.info(f"Using model {agent.api.model}")
    logger.info(f"{agent.name}: {agent.start_greeting}")

    while True:
        user_input = input("You: ")
        if not user_input.strip():
            user_input = "Alright, continue"

        if user_input.lower() == "exit":
            logger.info("Exiting AI Helper Chat Session.")
            break

        response = agent.update(user_input)

        logger.info(f"{agent.name}: {response}")
