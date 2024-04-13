import argparse

from chat_session import chat_session


def main():
    parser = argparse.ArgumentParser(description="AI Helper Command Line Interface")
    parser.add_argument("-q", "--query", type=str, help="Query to ask the AI helper")

    args = parser.parse_args()

    if args.query:
        print(f"Your query was: {args.query}")
        print("AI Response: This is where the AI's response will be generated.")
    else:
        chat_session()


if __name__ == "__main__":
    main()
