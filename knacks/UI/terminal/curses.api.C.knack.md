# Curses C API

## When To Load This Knack

Load this knack when you are writing or reviewing C code that uses the
portable curses interface directly. This is the right companion to
`curses.knack.md` when you need concrete entry points, core data types,
refresh semantics, or terminfo-facing calls.

## Relationship To Other Knacks

- `curses.knack.md` explains the portable screen-library model at a higher
  level.
- `ncurses.api.C.knack.md` is the better fit when the code depends on
  ncurses-specific extensions, wide-character variants beyond the portable
  subset, or ncurses utilities.

## Mental Model

The portable curses C API is declared through `<curses.h>` and revolves
around two kinds of state:
- process-wide screen state, such as `stdscr`, `curscr`, `LINES`, `COLS`,
  `COLORS`, and `COLOR_PAIRS`; and
- opaque handles such as `WINDOW *` and `SCREEN *`.

The library keeps a virtual screen and a physical-screen model. Most calls
mutate windows or library state. The actual terminal write usually happens
only when you call `refresh()`, `wrefresh()`, or the batched
`doupdate()` path.

Keep three layers distinct:
- curses window and screen objects;
- terminal capability data from terminfo; and
- the terminal emulator itself.

If something looks wrong, do not stop at the function name. Check the
active terminal description as well.

## Core Types And Globals

The standard header exposes a small set of types that drive the rest of the
API:
- `WINDOW` for window objects;
- `SCREEN` for terminal-screen contexts;
- `chtype` and `attr_t` for character-plus-attribute values;
- `cchar_t` and wide-character functions where the implementation supports
  the wide-character interfaces.

The portable global objects and variables matter operationally:
- `stdscr` is the default full-screen window.
- `curscr` is the library's view of the physical screen.
- `LINES` and `COLS` describe the current screen size after
  initialization.
- `COLORS` and `COLOR_PAIRS` become meaningful after `start_color()`.

Treat these as library state, not as independent sources of truth.

## API Families

### Startup And Teardown

The lifecycle entry points set up terminal mode, library state, and the
initial screen objects:
- `initscr()` for the common single-screen path;
- `newterm()`, `set_term()`, and `delscreen()` when you need explicit
  screen objects;
- `endwin()` and `isendwin()` to leave or test curses mode;
- `def_prog_mode()`, `def_shell_mode()`, `reset_prog_mode()`, and
  `reset_shell_mode()` when temporarily dropping back to the shell.

Prefer `newterm()` only when you really need more control. Most programs
should start with `initscr()`.

### Window And Pad Management

The window family provides the main object model:
- `newwin()`, `delwin()`, `mvwin()`, and `dupwin()` for independent
  windows;
- `subwin()` and `derwin()` for shared-content child windows;
- `newpad()`, `prefresh()`, and `pnoutrefresh()` for off-screen pads;
- `touchwin()`, `redrawwin()`, `syncok()`, `wsyncup()`, and `wsyncdown()`
  for repaint and synchronization behavior.

Remember that subwindows share underlying character storage. A repaint bug
in a child window can really be shared backing-state behavior.

### Output And Refresh

Most drawing calls come in families:
- character and string output such as `addch()`, `addstr()`, `waddnstr()`,
  `mvwaddstr()`, `printw()`, and `wprintw()`;
- border and line helpers such as `box()`, `border()`, `hline()`, and
  `vline()`;
- clear and erase operations such as `erase()`, `clrtoeol()`, and
  `clrtobot()`.

Separate mutation from flush:
- `wrefresh()` both stages and flushes one window;
- `wnoutrefresh()` stages without flushing;
- `doupdate()` flushes the staged virtual screen efficiently.

If you are updating multiple windows, prefer `wnoutrefresh()` followed by a
single `doupdate()`.

### Input And Terminal Modes

Input behavior is not just `getch()`:
- `getch()`, `wgetch()`, and `ungetch()` provide the base key path;
- `keypad()` enables translation of terminal escape sequences to `KEY_*`
  codes;
- `cbreak()`, `raw()`, `echo()`, `noecho()`, `halfdelay()`, `nodelay()`,
  and `timeout()` shape blocking and line discipline;
- `meta()` and `notimeout()` influence character width assumptions and ESC
  handling.

Keep `keypad()` and timeout settings near the code that reads from the
window. Input bugs often come from mode drift, not from the wrong key code.

### Attributes, Colors, And Wide Characters

The styling layer includes:
- attribute toggles such as `attron()`, `attroff()`, `standout()`, and
  their window-scoped `wattr_*` variants;
- color entry points such as `start_color()`, `init_pair()`,
  `pair_content()`, and `COLOR_PAIR()`;
- wide-character calls such as `setcchar()`, `wadd_wch()`, and
  `win_wch()` where the implementation exposes them.

Use the window-scoped forms when possible. They compose better than leaning
on the implicit `stdscr` context.

### Terminfo Access

Curses sits on top of terminal capability data, but the API also exposes
lower-level terminfo hooks:
- `setupterm()` to initialize terminal capability state;
- `tigetstr()`, `tigetnum()`, and `tigetflag()` to query capabilities;
- `tparm()` and `putp()` when you must format or emit capability strings
  directly.

This layer is useful when curses does not abstract a feature cleanly, but
every direct capability call narrows your portability story.

## Practical Guidance

Prefer the window-scoped variants in real programs. `waddstr(win, ...)` and
`wgetch(win)` make ownership clearer than bouncing through `stdscr`.

Keep initialization and teardown symmetrical. A typical safe sequence is:
- initialize with `initscr()`;
- configure input and echo modes immediately;
- run the main screen loop;
- call `endwin()` exactly once on the normal exit path.

Use the terminfo layer sparingly and deliberately. If the program starts to
mix a lot of `putp()` output with window-managed repainting, stop and
reassess the architecture.

## Sharp Edges

Many curses entry points may be implemented as macros. Avoid taking their
address or making assumptions that only hold for ordinary functions.

`KEY_*` values do not fit in an eight-bit `char`. Store input results in an
`int` or wider type.

Refresh semantics are easy to get wrong. Drawing calls usually modify only
library state. If nothing appears on screen, look for a missing
`wrefresh()` or `doupdate()` before assuming the draw call failed.

Wide-character correctness depends on locale and the implementation's wide
configuration. If Unicode or line-drawing output is broken, check locale,
terminfo, and the actual library build before blaming your application.

## Further Information

- X/Open `<curses.h>` reference:
  <https://pubs.opengroup.org/onlinepubs/7908799/xcurses/curses.h.html>
- X/Open terminfo reference:
  <https://pubs.opengroup.org/onlinepubs/7908799/xcurses/terminfo.html>
- ncurses `curs_initscr(3x)` manual:
  <https://invisible-island.net/ncurses/man/curs_initscr.3x.html>
- ncurses `curs_window(3x)` manual:
  <https://invisible-island.net/ncurses/man/curs_window.3x.html>
- ncurses `curs_getch(3x)` manual:
  <https://invisible-island.net/ncurses/man/curs_getch.3x.html>
- ncurses `curs_color(3x)` manual:
  <https://invisible-island.net/ncurses/man/curs_color.3x.html>
