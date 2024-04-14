from agent import Agent


def chat_session():
    print("AI Helper Chat Session. Type 'exit' to end the session.")
    agent = Agent()
    print(f"Using model {agent.api.model}")
    print(f"{agent.name}: {agent.start_greeting}")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting AI Helper Chat Session.")
            break

        response = agent.get_response(user_input)

        print(f"{agent.name}: {response}")
