"""
Example usage of the cprint function with colored output.
"""


from pyutils.colored import cprint, Palette
from typing import NamedTuple

# classic usage of cprint
cprint("Hello, World!").style(B=True)
cprint("This is a blue message.").style(Palette.BLUE)
cprint("This is a green message.").style(Palette.GREEN)
cprint("This is a warning message.").style(Palette.YELLOW)
cprint("This is an error message.").style(Palette.RED)
cprint("This is a bold message.").style(Palette.BOLD)
cprint("This is an underline message.").style(Palette.UNDERLINE)

# registering new colors
Palette.register("ORANGE_BOLD", "\033[38;5;208m\033[1m")
Palette.register("PURPLE_UNDERLINE", "\033[38;5;129m\033[4m")

# a usage pattern to use the colorized string in a more pythonic way
class C(NamedTuple):
    """
    A class to represent a colorized string.

    >>> C("This text will be green", Palette.GREEN)
    This text will be green
    """
    red: str = lambda text: Palette.RED.colorize(text)
    green: str = lambda text: Palette.GREEN.colorize(text)
    blue: str = lambda text: Palette.BLUE.colorize(text)
    B: str = lambda text: Palette.BOLD.colorize(text)
    U: str = lambda text: Palette.UNDERLINE.colorize(text)
    I: str = lambda text: Palette.ITALIC.colorize(text)

c = C()
c.green("This text will be green")
c.red("This text will be red")
c.B("This text will be bold")
c.U("This text will be underlined")
c.I("This text will be italic")

# directly using the colorized string in a more pythonic way
print(Palette.GREEN.colorize("This text will be green"))
print(Palette.RED.colorize("This text will be red"))
print(Palette.BOLD.colorize("This text will be bold"))
print(Palette.UNDERLINE.colorize("This text will be underlined"))
print(Palette.ITALIC.colorize("This text will be italic"))

# A semi coloured printing example
print("This is a message with multiple colors: " + Palette.GREEN.colorize("green") + ", " + Palette.RED.colorize("red") + ", and " + Palette.BLUE.colorize("blue") + ".")
print(f"This is a message with multiple colors: {Palette.GREEN.colorize('green')} , {Palette.RED.colorize('red')} and {Palette.BLUE.colorize('blue')} with fstrings.")
