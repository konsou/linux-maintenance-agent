import logging

from agent.agent import Agent
from agent.prompts import PLANNER_PROMPT, CLARIFICATION_PROMPT

logger = logging.getLogger(__name__)


def chat_session():
    logger.info("AI Helper Chat Session. Type 'exit' to end the session.")
    agent = Agent(name="Alice", system_prompt="", is_planner=False)
    # agent = Agent(name="Alice", system_prompt=PLANNER_PROMPT, is_planner=True)
    logger.info(f"Using model {agent.api.model}")
    logger.info(f"{agent.name}: {agent.start_greeting}")

    while True:
        user_input = input("You: ")
        if not user_input.strip():
            user_input = "Alright, continue"

        if user_input.lower() == "exit":
            logger.info("Exiting AI Helper Chat Session.")
            break

        response = agent.get_response(user_input)

        logger.info(f"{agent.name}: {response}")
