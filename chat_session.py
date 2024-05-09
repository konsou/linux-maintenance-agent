import logging

from agent.agent import Agent
from agent.prompts import PLANNER_PROMPT


def chat_session():
    logging.info("AI Helper Chat Session. Type 'exit' to end the session.")
    agent = Agent(name="Alice", system_prompt=PLANNER_PROMPT, is_planner=True)
    logging.info(f"Using model {agent.api.model}")
    logging.info(f"{agent.name}: {agent.start_greeting}")

    while True:
        user_input = input("You: ")
        if not user_input.strip():
            user_input = "Alright, continue"

        if user_input.lower() == "exit":
            logging.info("Exiting AI Helper Chat Session.")
            break

        response = agent.get_response(user_input)

        logging.info(f"{agent.name}: {response}")
