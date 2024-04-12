from agent import Agent
from llm_api.abc import Message


def chat_session():
    print("AI Helper Chat Session. Type 'exit' to end the session.")
    agent = Agent()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting AI Helper Chat Session.")
            break

        response = agent.get_response(user_input)

        print(f"AI Response: {response}")
