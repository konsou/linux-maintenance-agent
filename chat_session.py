from settings import LLM_API


def chat_session():
    print("AI Helper Chat Session. Type 'exit' to end the session.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting AI Helper Chat Session.")
            break
        
        response = LLM_API.response_from_prompt(user_input)
        print(f"AI Response: {response}")
