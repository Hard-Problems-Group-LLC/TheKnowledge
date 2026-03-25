# Curses Python API

## When To Load This Knack

Load this knack when you are writing Python code against the standard
`curses` module, or when you need to understand how Python's wrapper maps
onto the underlying curses or ncurses library.

## Relationship To Other Knacks

- `curses.knack.md` gives the higher-level screen-management model.
- `curses.api.C.knack.md` is the right companion when a Python behavior is
  really inherited from the underlying C library.
- `ncurses.api.C.knack.md` matters when you are diagnosing ncurses-specific
  behavior that leaks through Python's wrapper.

## Mental Model

Python's `curses` module is a fairly direct wrapper around the underlying
curses implementation. On most Unix-like systems, that means ncurses. The
module-level functions manage global library state, while window objects
expose most of the day-to-day drawing and input methods.

Think in three layers:
- module-level lifecycle functions such as `initscr()` and `wrapper()`;
- window methods such as `addstr()`, `getch()`, and `noutrefresh()`;
- helper modules such as `curses.ascii`, `curses.panel`, and
  `curses.textpad`.

Python keeps the C model visible rather than hiding it behind a different
object system. That is useful when you already know curses, but it also
means the old constraints still matter.

## Module And Object Map

The main `curses` module handles lifecycle, colors, terminals, and window
creation. A `window` object handles most drawing and input. The companion
modules fill specific gaps:
- `curses.ascii` provides ASCII constants and classification helpers;
- `curses.panel` adds a stacking model on top of windows;
- `curses.textpad` adds a simple editable text widget and rectangle helper.

Treat `curses.panel` as a layout primitive, not as a full widget toolkit.
Treat `curses.textpad` as a convenience layer, not as a general TUI
framework.

## API Families

### Lifecycle And Setup

The common lifecycle entry points are:
- `curses.wrapper()` for the safest top-level program structure;
- `curses.initscr()` and `curses.endwin()` for manual lifecycle control;
- `curses.newwin()` and `curses.newpad()` to allocate windows and pads;
- `curses.start_color()`, `curses.use_default_colors()`, and
  `curses.assume_default_colors()` for color setup.

Prefer `wrapper()` unless you have a concrete reason to manage teardown
yourself. It restores terminal state even when an exception escapes.

### Window Methods

Most real work happens on window objects:
- output calls such as `addch()`, `addstr()`, `insstr()`, `hline()`,
  `vline()`, and `border()`;
- movement and repaint calls such as `move()`, `clear()`, `erase()`,
  `refresh()`, and `noutrefresh()`;
- hierarchy calls such as `subwin()` and `derwin()`;
- input calls such as `getch()`, `getkey()`, `get_wch()`, and `instr()`.

The Python wrapper mirrors the C refresh model closely. If multiple windows
update in one pass, use `noutrefresh()` on each and then call
`curses.doupdate()` once.

### Input, Modes, And Keys

The module-level mode functions still matter in Python:
- `cbreak()`, `raw()`, `echo()`, `noecho()`, `halfdelay()`, and `nl()`;
- `mousemask()` and mouse constants when mouse reporting is enabled;
- `ungetch()` and `unget_wch()` for pushing input back.

On windows, `keypad(True)` is still the switch that tells curses to decode
multibyte terminal escape sequences into logical key codes.

Use `get_wch()` when you care about wide-character input. Keep the return
value in a type that can handle both ordinary characters and `KEY_*`
integers.

### Attributes And Colors

The attribute and color path is mostly module-scoped constants plus window
methods:
- attributes such as `A_BOLD`, `A_REVERSE`, `A_UNDERLINE`, and ACS glyphs;
- color helpers such as `color_pair()`, `pair_number()`, `init_pair()`,
  and `pair_content()`;
- screen metrics such as `LINES`, `COLS`, `COLORS`, and `COLOR_PAIRS`.

These values become valid only after initialization. Do not read `LINES` or
`COLORS` before `initscr()` and `start_color()`.

### Helper Modules

`curses.ascii` is useful for normalizing control-key handling and checking
raw byte values without depending on locale-sensitive string logic.

`curses.panel` lets windows overlap with explicit depth. The crucial call is
`curses.panel.update_panels()`, followed by `curses.doupdate()`.

`curses.textpad.Textbox` is a narrow but handy convenience for simple text
entry fields. It is usually enough for small prompts and editors, but it is
not a replacement for a full application event model.

## Practical Guidance

Call `locale.setlocale(locale.LC_ALL, '')` early if you want Unicode to
behave sanely. Python's wrapper inherits the underlying library's locale
expectations.

Prefer strings over manual byte juggling unless you are debugging terminal
encoding problems. Python's wrapper accepts Unicode strings for many output
calls, but the underlying terminal and library configuration still decide
what ultimately renders.

Check `curses.ncurses_version` when behavior appears to depend on the linked
ncurses version. That field exists only when Python is actually using
ncurses.

## Sharp Edges

`curses.error` is the common exception when the wrapped C call returns an
error. The message is usually short, so pair the exception site with window
dimensions, cursor coordinates, and current mode when debugging.

The module is Unix-oriented. Availability varies across platforms, and the
standard documentation explicitly excludes several targets.

Window coordinates are still y-first, x-second. Python does not normalize
that away.

A panel object must stay referenced. If the last Python reference to a panel
disappears, it can be garbage-collected and removed from the panel stack.

## Further Information

- Python `curses` library reference:
  <https://docs.python.org/3/library/curses.html>
- Python `curses.panel` reference:
  <https://docs.python.org/3/library/curses.panel.html>
- Python `curses.ascii` reference:
  <https://docs.python.org/3.9/library/curses.ascii.html>
- Python curses HOWTO:
  <https://docs.python.org/3.11/howto/curses.html>
- Python curses C API for extension authors:
  <https://docs.python.org/3/c-api/curses.html>
