from collections import namedtuple
from enum import Enum


__all__ = [
    'cprint',
    'Colors'
]

class Colors(str, Enum):
    """Enumeration of text colors for terminal output."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = PALE = "\033[93m"
    FAIL = RED = "\033[91m"
    ENDC = RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ITALIC = "\033[3m"
    ORANGE = "\033[38;5;208m"
    PURPLE = "\033[38;5;129m"

    def colorize(self, text: str,) -> str:
        """
        Colorize the given text with the color represented by this enum member.

        >>> Colors.GREEN.colorize("This text will be green")
        This text will be green

        >>> Colors.FAIL.colorize("This text will be red")
        This text will be red

        >>> Colors.GREEN.colorize(Colors.BOLD.colorize("This text will be bold and green"))
        This text will be bold and green
        """
        return f"{self.value}{text}{Colors.ENDC.value}"

    @classmethod
    def register(cls, name: str, color_code: str):
        """
        Register a new color or style with the given name and color code.

        >>> Colors.register("MAGENTA", "\033[35m")
        >>> Colors.MAGENTA.colorize("This text will be magenta")
        This text will be magenta
        """
        setattr(cls, name, color_code)


def cprint(*args, **kwargs):
    """Extention to python.print
    Provides extention functions for various color printing.
    """
    colorfunc = namedtuple(
        "colorfunc",
        """
            header,
            blue,
            cyan,
            green,
            warning,
            fail,
            bold,
            underline
        """,
    )

    return colorfunc(
        lambda: print(Colors.HEADER.value, *args, Colors.ENDC.value, **kwargs),
        lambda: print(Colors.BLUE.value, *args, Colors.ENDC.value, **kwargs),
        lambda: print(Colors.CYAN.value, *args, Colors.ENDC.value, **kwargs),
        lambda: print(Colors.GREEN.value, *args, Colors.ENDC.value, **kwargs),
        lambda: print(Colors.WARNING.value, *args, Colors.ENDC.value, **kwargs),
        lambda: print(Colors.FAIL.value, *args, Colors.ENDC.value, **kwargs),
        lambda: print(Colors.BOLD.value, *args, Colors.ENDC.value, **kwargs),
        lambda: print(Colors.UNDERLINE.value, *args, Colors.ENDC.value, **kwargs),
    )


# tests:
def _cprint_tests():
    import io

    test_input = ("ankit", "\t", "yadav", "C- ", 24)
    print_op, cprint_op = io.StringIO(""), io.StringIO("")

    slice_color_characters = slice(
        len(Colors.HEADER.value) + 1, -(1 + len(Colors.ENDC.value) + 1)
    )
    # test1 : testing if all the character outputs are same for `print` and `cprint`
    cprint(*test_input, file=cprint_op).header()
    print(*test_input, file=print_op)
    assert (
        print_op.getvalue()[:-1] == cprint_op.getvalue()[slice_color_characters]
    ), "Difference in characters"

    cprint("All Tests Working Fine !!").bold()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        if len(sys.argv) > 2:
            if sys.argv[2].lower() == "cprint":
                _cprint_tests()
        else:
            print(
                f"""
                Modules Aavailable For Testing :
                
                    1. cprint
            """
            )
