import argparse

from chat_session import chat_session



def main():
    parser = argparse.ArgumentParser(description="AI Helper Command Line Interface")
    parser.add_argument('-q', '--query', type=str, help='Query to ask the AI helper')
    
    args = parser.parse_args()
    
    if args.query:
        # If a query is provided as an argument, handle it as before
        print(f"Your query was: {args.query}")
        print("AI Response: This is where the AI's response will be generated.")
    else:
        # If no query argument is provided, start the chat session
        chat_session()

if __name__ == "__main__":
    main()
