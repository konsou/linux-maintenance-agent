from colorama import Fore, Style, init
from colorama import Fore as Color

# Initialize colorama to auto-reset colors back to default after each print statement
init(autoreset=True)


def print_in_color(message: str, color: str):
    """
    Prints the given message in the specified color.

    Args:
        message (str): The message to print.
        color (Color): The color to print the message in.
    """
    print(f"{color}{message}{Style.RESET_ALL}")


if __name__ == '__main__':
    print_in_color("Test", Fore.BLACK)
