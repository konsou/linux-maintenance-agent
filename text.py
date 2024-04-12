from colorama import Fore, Style, init

# Initialize colorama to auto-reset colors back to default after each print statement
init(autoreset=True)

class Color:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL

def print_in_color(message: str, color: Color):
    """
    Prints the given message in the specified color.

    Args:
        message (str): The message to print.
        color (Color): The color to print the message in.
    """
    print(f"{color}{message}{Color.RESET}")
