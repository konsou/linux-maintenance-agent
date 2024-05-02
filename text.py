from colorama import Fore, Style
from colorama import Fore as Color


def print_in_color(message: str, color: str):
    """
    Prints the given message in the specified color.

    Args:
        message (str): The message to print.
        color (Color): The color to print the message in.
    """
    print(f"{color}{message}{Style.RESET_ALL}")


def truncate_string(s: str, n: int) -> str:
    if len(s) > n:
        return s[:n] + "..."
    return s


if __name__ == "__main__":
    print_in_color("Test", Fore.BLACK)
