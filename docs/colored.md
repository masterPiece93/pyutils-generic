# `colored.py` — Documentation

A small, **dependency-free** toolkit for styling terminal text with ANSI escape
codes. It gives you discoverable color/effect enums plus two ergonomic APIs for
applying them: the `Styleit` operator syntax and a `print`-compatible `cprint`.

- **No third-party dependencies** — pure standard library (`enum`, `typing`, `argparse`, `doctest`).
- **Single file** — just drop `colored.py` into your project.
- **Type-friendly** — colors and effects are real `Enum` members.

---

## Table of contents

1. [Requirements](#requirements)
2. [Installation / adding to a codebase](#installation--adding-to-a-codebase)
3. [Core concepts](#core-concepts)
4. [Quick start](#quick-start)
5. [API reference](#api-reference)
   - [`Palette`](#palette)
   - [`Palette.colorize`](#palettemembercolorizetext)
   - [`Palette.register`](#paletteregistername-code)
   - [`Effects`](#effects)
   - [`Styleit`](#styleit)
   - [`cprint`](#cprint)
6. [Recipes](#recipes)
7. [Running as a script (demo & doctests)](#running-as-a-script-demo--doctests)
8. [Gotchas & tips](#gotchas--tips)
9. [FAQ](#faq)

---

## Requirements

- Python **3.10+** (the code uses `str | Palette` union syntax).
- An ANSI-capable terminal for the colors to render. Most modern terminals
  qualify (Linux/macOS terminals, Windows Terminal, VS Code integrated
  terminal). Some effects like blink, framed, encircled and overline are not
  supported everywhere.

---

## Installation / adding to a codebase

`colored.py` is a single, self-contained module. There are a few ways to use it.

### Option 1 — Vendor the file (simplest)

Copy `colored.py` into your project, e.g. into a `utils/` package:

```
your_project/
├── your_project/
│   ├── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── colored.py      <-- copied here
│   └── app.py
```

Then import from it:

```python
from your_project.utils.colored import cprint, Palette, Effects, Styleit
```

### Option 2 — Keep it at the project root

If your entry scripts live at the repo root, you can import directly:

```python
from colored import cprint, Palette, Effects
```

### Option 3 — Add its folder to `sys.path`

If the file lives in a shared location:

```python
import sys
sys.path.append("/home/ubuntu/Documents/personal/python_colored")

from colored import cprint, Palette
```

### Recommended import

For day-to-day use you usually only need three names:

```python
from colored import cprint, Palette, Effects
```

Add `Styleit` if you prefer the `style >> text` operator form.

---

## Core concepts

The module is built from `enum.Enum` classes so everything is discoverable and
autocompletes in editors.

| Name | What it is |
| --- | --- |
| `ForegroundStandardANSI` / `BackgroundStandardANSI` | The 8 standard fg/bg colors. |
| `ForegroundBrightStandardANSI` / `BackgroundBrightStandardANSI` | Bright variants. |
| `*RgbANSI` / `*HexANSI` / `*HslANSI` | Truecolor (24-bit) sample colors. |
| `StandardANSI` | Merge of the four standard/bright enums. |
| `Effects` | Text style codes (bold, dim, italic, underline, blink, reverse, hidden, strikethrough, …) with matching `*_OFF` reset codes. |
| **`Palette`** | The single combined enum containing **all** colors + effects, plus `ENDC`/`RESET`. This is what you use most. |
| `Styleit` | Helper implementing `style >> text`. |
| `cprint` | A `print` replacement with a fluent `.style(...)`. |

The reset sequence `\033[0m` is available as `Palette.ENDC` and `Palette.RESET`.

---

## Quick start

```python
from colored import cprint, Palette, Effects, Styleit

# 1) Wrap a string with a color
print(Palette.GREEN.colorize("success"))

# 2) print() replacement with fluent styling
cprint("Warning!").style(color=Palette.YELLOW, B=True)

# 3) Operator style
print(Styleit(Palette.RED, U=True) >> "underlined red")

# 4) Effects
cprint("blinking").style(color=Palette.RED, blink=True)
```

---

## API reference

### `Palette`

The combined enum of every color and effect. Access members by name:

```python
Palette.RED            # standard foreground red
Palette.BG_YELLOW      # standard yellow background
Palette.BRIGHT_GREEN   # bright foreground green
Palette.BG_BRIGHT_BLUE # bright background blue
Palette.RED_RGB        # 24-bit truecolor sample
Palette.BOLD           # effect (from Effects, merged in)
Palette.ENDC           # reset ("\033[0m")
Palette.RESET          # alias of ENDC
```

Each member's `.value` is the raw escape string, e.g. `Palette.RED.value == "\033[31m"`.

#### `Palette.<MEMBER>.colorize(text)`

Wrap `text` in the member's escape code plus a trailing reset (`ENDC`). Because
it always appends a reset, calls can be **nested safely**:

```python
Palette.GREEN.colorize("hi")
# -> "\033[32mhi\033[0m"

# Combine a background and a foreground by nesting
Palette.BG_YELLOW.colorize(Palette.RED.colorize("red on yellow"))
```

#### `Palette.register(name, code)`

Register a brand new color/effect on the `Palette` enum **at runtime**. Returns
the created (or aliased) enum member.

```python
Palette.register("BRAND_PURPLE", "\033[38;2;123;45;67m")

cprint("branded").style(color=Palette.BRAND_PURPLE)
# or reference by name:
cprint("branded").style(color="BRAND_PURPLE")
```

Notes:
- Registering an existing **name** raises `ValueError`.
- Registering a **code** that already exists reuses the existing member as an alias.
- A good place to register your palette is once at import time in a small setup module.

### `Effects`

The style/effect codes. Every effect has an `*_OFF` reset counterpart.

| Member | Code | Notes |
| --- | --- | --- |
| `BOLD` | `1` | |
| `DIM` | `2` | faint |
| `ITALIC` | `3` | |
| `UNDERLINE` | `4` | |
| `BLINK` | `5` | not supported everywhere |
| `RAPID_BLINK` | `6` | rarely supported |
| `REVERSE` | `7` | inverse video (swaps fg/bg) |
| `HIDDEN` | `8` | concealed |
| `STRIKETHROUGH` | `9` | |
| `DOUBLE_UNDERLINE` | `21` | |
| `FRAMED` / `ENCIRCLED` / `OVERLINE` | `51` / `52` / `53` | limited support |

Off-codes: `BOLD_OFF` (`22`), `DIM_OFF` (`22`), `ITALIC_OFF` (`23`),
`UNDERLINE_OFF` (`24`), `BLINK_OFF` (`25`), `REVERSE_OFF` (`27`),
`HIDDEN_OFF` (`28`), `STRIKETHROUGH_OFF` (`29`), `FRAMED_OFF` (`54`),
`OVERLINE_OFF` (`55`).

These effects are also merged into `Palette`, so `Palette.BOLD` works too.

### `Styleit`

A helper class that applies a style to text using the `>>` operator.

```python
Styleit(style_code, bg_color=None, B=False, U=False, I=False,
        dim=False, blink=False, reverse=False, hidden=False,
        strikethrough=False, effects=None)
```

| Parameter | Meaning |
| --- | --- |
| `style_code` | Foreground color/effect — a `Palette`/`Effects` member or a raw escape string. |
| `bg_color` | Background color (member or raw string). |
| `B`, `U`, `I` | Bold, underline, italic. |
| `dim`, `blink`, `reverse`, `hidden`, `strikethrough` | Additional effect flags. |
| `effects` | List of extra `Effects` members/names/codes. |

Apply with `>>`:

```python
print(Styleit(Palette.RED, B=True, U=True) >> "bold underlined red")
print(Styleit(Palette.BLUE, I=True) >> "italic blue")
print(Styleit(Palette.BRIGHT_GREEN, bg_color=Palette.BG_BRIGHT_YELLOW) >> "green on yellow")
```

`Styleit(...) >> text` returns the styled **string** (it does not print), so it
composes with `print`, logging, f-strings, etc.

### `cprint`

A drop-in replacement for the built-in `print` with an optional fluent
`.style(...)` call.

```python
cprint(*values, sep=" ", end="\n", file=None, flush=False)
```

Used on its own, it behaves exactly like `print`:

```python
cprint("hello", "world")            # "hello world\n"
cprint("no newline", end="")        # like print(..., end="")
```

Chain `.style(...)` to color/format the text instead:

```python
cprint("text").style(
    color=None,             # foreground: Palette/Effects member, name, or raw code
    bg_color=None,          # background
    B=False, U=False, I=False,        # bold / underline / italic
    dim=False, blink=False, rapid_blink=False,
    reverse=False, hidden=False, strikethrough=False,
    double_underline=False, overline=False, framed=False, encircled=False,
    effects=None,           # list of extra Effects members/names/codes
)
```

Examples:

```python
cprint("Bold red on yellow bg").style(B=True, color=Palette.RED, bg_color=Palette.BG_YELLOW)
cprint("Blinking").style(color=Palette.RED, blink=True)
cprint("Mixed").style(color=Palette.CYAN, effects=[Effects.BOLD, Effects.UNDERLINE, Effects.BLINK])
cprint("By name").style(color="BRIGHT_GREEN", U=True)
```

**How printing works (important):** printing is *deferred*.

- If you chain `.style(...)`, the **styled** text is printed.
- If you don't, the **plain** text is printed when the temporary `cprint`
  object is discarded (via `__del__`).

For the common one-liner pattern `cprint("x").style(...)` this behaves exactly
as expected. See [Gotchas](#gotchas--tips) for the edge case where you assign
the result to a variable.

---

## Recipes

### A tiny logging helper

```python
from colored import cprint, Palette

def info(msg):    cprint(f"[INFO]  {msg}").style(color=Palette.BLUE)
def ok(msg):      cprint(f"[OK]    {msg}").style(color=Palette.GREEN, B=True)
def warn(msg):    cprint(f"[WARN]  {msg}").style(color=Palette.YELLOW, B=True)
def error(msg):   cprint(f"[ERROR] {msg}").style(color=Palette.RED, B=True, bg_color=Palette.BG_BRIGHT_BLACK)

info("starting up")
ok("connected")
warn("retrying")
error("could not connect")
```

### Register your brand colors once

```python
# brand.py
from colored import Palette

Palette.register("BRAND_PRIMARY",  "\033[38;2;16;185;129m")   # teal
Palette.register("BRAND_ACCENT",   "\033[38;2;245;158;11m")   # amber

# elsewhere
from colored import cprint
import brand  # ensures colors are registered

cprint("Brand!").style(color="BRAND_PRIMARY", B=True)
```

### Build styled strings for f-strings / logging

```python
from colored import Palette, Styleit

label = Styleit(Palette.GREEN, B=True) >> "PASS"
print(f"Test result: {label}")
```

### Reset a nested section manually

```python
from colored import Palette

parts = [
    Palette.RED.value, "error",
    Palette.RESET.value, " normal again",
]
print("".join(parts))
```

---

## Running as a script (demo & doctests)

The module has a CLI entry point built with `argparse`.

```bash
# Print styled demo output (default)
python colored.py
python colored.py --mode demo

# Run the embedded doctests
python colored.py --mode doctest

# Verbose doctests
python colored.py --mode doctest --verbose
```

Options:

| Flag | Values | Description |
| --- | --- | --- |
| `-m`, `--mode` | `demo` \| `doctest` | Choose demo output (default) or run doctests. |
| `-v`, `--verbose` | — | Verbose output (doctest mode only). |

The process exit code equals the number of failed doctests, which is convenient
for CI pipelines:

```bash
python colored.py --mode doctest && echo "docs OK"
```

To inspect the raw escape codes instead of rendered colors, pipe through
`cat -v`:

```bash
python colored.py --mode demo | cat -v
```

---

## Gotchas & tips

- **Deferred `cprint` printing.** If you assign a `cprint(...)` to a variable
  without calling `.style(...)`, the plain text is printed only when that
  variable is garbage-collected/goes out of scope:

  ```python
  x = cprint("hi")     # nothing printed yet
  # ...
  del x                # "hi" prints here (or at scope exit)
  ```

  For normal usage (`cprint("hi")` or `cprint("hi").style(...)`) this is a
  non-issue.

- **Terminal support varies.** `blink`, `rapid_blink`, `framed`, `encircled`,
  `overline` and sometimes `strikethrough` may not render. The correct codes
  are always emitted regardless.

- **Redirection / non-TTY output.** When output is redirected to a file or a
  non-ANSI consumer, the escape codes are written literally. If you need to
  disable coloring when not attached to a TTY, guard your calls with
  `sys.stdout.isatty()` and fall back to `print`.

- **Windows.** Use Windows Terminal or enable virtual terminal processing.
  Modern Windows 10+ terminals generally support ANSI out of the box.

- **`Styleit` vs `cprint`.** Use `Styleit` when you need the styled **string**
  (for logging, f-strings, storing). Use `cprint` when you want to **print**
  directly.

---

## FAQ

**Q: Do I need to install anything?**
No. It is pure standard library — just add the `colored.py` file.

**Q: How do I use a custom RGB color?**
Register it: `Palette.register("MY_COLOR", "\033[38;2;R;G;Bm")`, then reference
`Palette.MY_COLOR` or the string `"MY_COLOR"`.

**Q: How do I turn off a single effect without resetting everything?**
Use the matching off-code, e.g. `Effects.UNDERLINE_OFF` (`\033[24m`).

**Q: Can I style multi-argument output like `print(a, b, c)`?**
Yes: `cprint(a, b, c, sep=", ").style(color=Palette.CYAN)`.

**Q: Does `Styleit(...) >> text` print?**
No — it returns a string. Pass it to `print()` or use `cprint` if you want it
printed directly.