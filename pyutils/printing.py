from collections import namedtuple
from enum import Enum


__all__ = [
    'cprint',
]

class Colors(str, Enum):
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


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
