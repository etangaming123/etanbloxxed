"""Small stand-alone helpers shared across the package."""
import logging
import random

from .constants import IDLE_TEXTS, RARE_IDLE_CHANCE, RARE_IDLE_TEXT

logger = logging.getLogger("etanbloxxed")


def configure_logging(debug: bool = False) -> None:
    """Set up logging. Pass --debug on the command line to see debug output."""
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO, format="%(message)s")


def print_temporary(text: str) -> None:
    """Print a line that gets overwritten by the next print/print_temporary call."""
    print(text, end="\r")


def clear_line() -> None:
    print(" " * 80, end="\r")


def ask_yes_no(prompt: str) -> bool:
    yes_answers = {"yes", "y", "true", "yeah"}
    no_answers = {"no", "n", "false", "nah"}
    while True:
        answer = input(prompt).strip().lower()
        if answer in yes_answers:
            return True
        if answer in no_answers:
            return False
        print("Could not tell if that was a yes or no")


def get_random_idle_text() -> str:
    if random.randint(1, RARE_IDLE_CHANCE) == RARE_IDLE_CHANCE:
        print("1 in 33 chance!")
        return RARE_IDLE_TEXT
    return random.choice(IDLE_TEXTS)
