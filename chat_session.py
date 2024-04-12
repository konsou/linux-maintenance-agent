from settings import LLM_API
from llm_api.abc import Message

def chat_session():
    print("AI Helper Chat Session. Type 'exit' to end the session.")
    
    # Initialize an empty list to store messages.
    chat_history = []
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting AI Helper Chat Session.")
            break
        
        # Add the user's message to the chat history.
        chat_history.append(Message(role="user", content=user_input))
        
        # Assuming LLM_API is an instance of OpenRouterAPI or similar that can handle a list of Message objects.
        response = LLM_API.response_from_messages(chat_history)
        
        # Add the AI's response to the chat history.
        chat_history.append(Message(role="assistant", content=response))
        
        print(f"AI Response: {response}")

