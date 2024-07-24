import random

from pyfiglet import Figlet

# Color definitions
MAIN = "\033[38;5;50m"
PLOAD = "\033[38;5;119m"
GREEN = "\033[38;5;47m"
BLUE = "\033[0;38;5;12m"
ORANGE = "\033[0;38;5;214m"
RED = "\033[1;31m"
END = "\033[0m"
BOLD = "\033[1m"

# Character designs
A = [["", "┌", "─", "┐"], ["", "├", "─", "┤"], ["", "┴", " ", "┴"]]
B = [["", "┌", "─", "┐"], ["", "├", "─", "┤"], ["", "└", "─", "┘"]]
C = [["", "┌", "─", "┐"], ["", "│", " ", " "], ["", "└", "─", "┘"]]
D = [["", "┌", "─", "┐"], ["", "│", " ", "│"], ["", "└", "─", "┘"]]
E = [["", "┌", "─", "┐"], ["", "├", "─", " "], ["", "└", "─", "┘"]]
F = [["", "┌", "─", "┐"], ["", "├", "─", "┤"], ["", "│", " ", " "]]
G = [["", "┌", "─", "┐"], ["", "│", "─", "┤"], ["", "└", "─", "┘"]]
H = [["", "│", " ", "│"], ["", "├", "─", "┤"], ["", "│", " ", "│"]]
I = [["", "┌", "─", "┐"], ["", " ", "│", " "], ["", "└", "─", "┘"]]
J = [["", " ", "┌", "┐"], ["", " ", "│", "│"], ["", "└", "─", "┘"]]
K = [["", "│", "┌", "│"], ["", "├", "┤", " "], ["", "│", "└", "│"]]
L = [["", "│", " ", " "], ["", "│", " ", " "], ["", "└", "─", "┘"]]
M = [["", "│", "│", "│"], ["", "├", "┴", "┤"], ["", "│", " ", "│"]]
N = [["", "│", " ", "│"], ["", "├", "┬", "┤"], ["", "│", " ", "│"]]
O = [["", "┌", "─", "┐"], ["", "│", " ", "│"], ["", "└", "─", "┘"]]
P = [["", "┌", "─", "┐"], ["", "├", "─", "┤"], ["", "│", " ", " "]]
Q = [["", "┌", "─", "┐"], ["", "│", "┌", "│"], ["", "└", "┘", "┘"]]
R = [["", "┌", "─", "┐"], ["", "├", "─", "┤"], ["", "│", "└", "│"]]
S = [["", "┌", "─", "┐"], ["", "└", "─", "┐"], ["", "└", "─", "┘"]]
T = [["", "┌", "─", "┐"], ["", " ", "│", " "], ["", " ", "│", " "]]
U = [["", "│", " ", "│"], ["", "│", " ", "│"], ["", "└", "─", "┘"]]
V = [["", "│", " ", "│"], ["", "│", " ", "│"], ["", " ", "┴", " "]]
W = [["", "│", " ", "│"], ["", "│", " ", "│"], ["", "└", "┴", "┘"]]
X = [["", "│", " ", "│"], ["", " ", "┼", " "], ["", "│", " ", "│"]]
Y = [["", "│", " ", "│"], ["", " ", "┼", " "], ["", " ", "│", " "]]
Z = [["", "┌", "─", "┐"], ["", " ", "┼", " "], ["", "└", "─", "┘"]]
ZERO = [[" ", "┌", "─", "┐"], [" ", "│", " ", "│"], [" ", "└", "─", "┘"]]
ONE = [[" ", " ", "┌", "┐"], [" ", " ", "│", "│"], [" ", " ", "└", "┘"]]
TWO = [[" ", "┌", "─", "┐"], [" ", "┌", "─", "┘"], [" ", "└", "─", "┘"]]
THREE = [[" ", "┌", "─", "┐"], [" ", "┌", "─", "┘"], [" ", "└", "─", "┘"]]
FOUR = [[" ", "│", " ", "│"], [" ", "└", "─", "┤"], [" ", " ", " ", "│"]]
FIVE = [[" ", "┌", "─", "┐"], [" ", "└", "─", "┐"], [" ", "└", "─", "┘"]]
SIX = [[" ", "┌", "─", "┐"], [" ", "├", "─", "┐"], [" ", "└", "─", "┘"]]
SEVEN = [[" ", "┌", "─", "┐"], [" ", " ", " ", "│"], [" ", " ", " ", "│"]]
EIGHT = [[" ", "┌", "─", "┐"], [" ", "├", "─", "┤"], [" ", "└", "─", "┘"]]
NINE = [[" ", "┌", "─", "┐"], [" ", "├", "─", "┤"], [" ", "└", "─", "┘"]]

SPACE = [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]]

# Mapping characters to designs
CHAR_MAP = {
    "A": A,
    "B": B,
    "C": C,
    "D": D,
    "E": E,
    "F": F,
    "G": G,
    "H": H,
    "I": I,
    "J": J,
    "K": K,
    "L": L,
    "M": M,
    "N": N,
    "O": O,
    "P": P,
    "Q": Q,
    "R": R,
    "S": S,
    "T": T,
    "U": U,
    "V": V,
    "W": W,
    "X": X,
    "Y": Y,
    "Z": Z,
    "0": ZERO,
    "1": ONE,
    "2": TWO,
    "3": THREE,
    "4": FOUR,
    "5": FIVE,
    "6": SIX,
    "7": SEVEN,
    "8": EIGHT,
    "9": NINE,
    " ": SPACE,
}

FIGLET_FONTS = [
    "3-d",
    "3x5",
    "5lineoblique",
    "acrobatic",
    "alligator",
    "alligator2",
    "alphabet",
    "avatar",
    "banner",
    "banner3-D",
    "banner3",
    "banner4",
    "barbwire",
    "basic",
    "bell",
    "big",
    "bigchief",
    "binary",
    "block",
]


def print_banner(text):
    """
    Print a colorful banner
    :param text:  The text to bannerize
    """

    # Initialize final output list
    banner = []
    print("\r")
    init_color = 36
    txt_color = init_color
    cl = 0

    for charset in range(3):  # Each character design has 3 rows
        for letter in text.upper():
            # Fetch the design for the current letter or use SPACE as default if not found
            char_design = CHAR_MAP.get(letter, SPACE)

            for i in range(len(char_design[charset])):
                clr = f"\033[38;5;{txt_color}m"
                char = f"{clr}{char_design[charset][i]}"
                banner.append(char)
                cl += 1
                txt_color = txt_color + 36 if cl <= 3 else txt_color

            cl = 0
            txt_color = init_color

        init_color += 31
        if charset < 2:
            banner.append("\n")

    # Print final output
    print(f"{''.join(banner).strip()}{END}")


def print_random_banner(text):
    """
    Prints a random banner
    :param text: The text to bannerize
    """

    # Use random.choice() to select between the following:
    # 1. print_random_banner()
    # 2. Print a print_banner()
    choice = random.choice([1, 2])

    if choice == 1:
        # Remove special characters from the text
        # Except for spaces
        for char in text:
            if not char.isalnum() and char != " ":
                text = text.replace(char, "")

        print_banner(text)
        return

    # Using random.choice() to select a random character design
    # from the FIGLET_FONTS list
    font = random.choice(FIGLET_FONTS)

    # Using the figlet library to print the banner
    figlet = Figlet(font=font)

    # Obtaining the banner
    banner = figlet.renderText(text)

    # Printing the banner
    print(banner)
