"""
Example usage of the cprint function with colored output.
"""


from pyutils.printing import cprint, Colors
from typing import NamedTuple

# classic usage of cprint
cprint("Hello, World!").header()
cprint("This is a blue message.").blue()
cprint("This is a green message.").green()
cprint("This is a warning message.").warning()
cprint("This is an error message.").fail()
cprint("This is a bold message.").bold()
cprint("This is an underline message.").underline()

# registering new colors
Colors.register("ORANGE_BOLD", "\033[38;5;208m\033[1m")
Colors.register("PURPLE_UNDERLINE", "\033[38;5;129m\033[4m")

# a usage pattern to use the colorized string in a more pythonic way
class C(NamedTuple):
    """
    A class to represent a colorized string.

    >>> C("This text will be green", Colors.GREEN)
    This text will be green
    """
    red: str = lambda text: Colors.RED.colorize(text)
    green: str = lambda text: Colors.GREEN.colorize(text)
    blue: str = lambda text: Colors.BLUE.colorize(text)
    B: str = lambda text: Colors.BOLD.colorize(text)
    U: str = lambda text: Colors.UNDERLINE.colorize(text)
    I: str = lambda text: Colors.ITALIC.colorize(text)

c = C()
c.green("This text will be green")
c.red("This text will be red")
c.B("This text will be bold")
c.U("This text will be underlined")
c.I("This text will be italic")

# directly using the colorized string in a more pythonic way
print(Colors.GREEN.colorize("This text will be green"))
print(Colors.RED.colorize("This text will be red"))
print(Colors.BOLD.colorize("This text will be bold"))
print(Colors.UNDERLINE.colorize("This text will be underlined"))
print(Colors.ITALIC.colorize("This text will be italic"))

# A semi coloured printing example
print("This is a message with multiple colors: " + Colors.GREEN.colorize("green") + ", " + Colors.RED.colorize("red") + ", and " + Colors.BLUE.colorize("blue") + ".")
print(f"This is a message with multiple colors: {Colors.GREEN.colorize("green")} , {Colors.RED.colorize("red")} and {Colors.BLUE.colorize("blue")} with fstrings.")
