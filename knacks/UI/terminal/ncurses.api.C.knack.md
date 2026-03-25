# ncurses C API

## When To Load This Knack

Load this knack when the code is written against ncurses specifically, or
when a supposedly portable curses program is really depending on ncurses
extensions, utilities, wide-character interfaces, or side libraries.

## Relationship To Other Knacks

- `ncurses.knack.md` explains the implementation boundary and operational
  model.
- `curses.api.C.knack.md` is the portable baseline.
- `ncurses.api.CPP.knack.md` covers the shipped C++ wrapper layer rather
  than the plain C entry points.

## Mental Model

The ncurses C API is the portable curses model plus a large body of
implementation detail:
- the core screen and window calls in `<curses.h>`;
- wide-character interfaces and extra helpers in the wide build;
- extension families such as resize management, default-color helpers,
  extra key handling, and mouse support;
- side libraries for panels, menus, and forms; and
- terminfo tools such as `tic`, `infocmp`, `toe`, and `tput`.

That means "uses ncurses" can mean very different things. Some programs use
only the portable subset but happen to link ncurses. Others rely on
`NCURSES_VERSION`, `use_default_colors()`, `resizeterm()`, or wide-character
calls that are not a portable baseline.

## Build And Header Layout

The common header remains `<curses.h>`. Side libraries add:
- `<panel.h>` for stacked windows;
- `<menu.h>` for menu support;
- `<form.h>` for forms.

In practice you also need to choose narrow versus wide builds. Modern code
usually wants the wide-character libraries such as `libncursesw`, together
with `libpanelw`, `libmenuw`, and `libformw` as needed.

Keep the implementation boundary explicit in build files. If the code uses
ncurses-only entry points, say so instead of advertising generic curses.

## API Families

### Core Lifecycle And Windows

The lifecycle and window model start with the usual curses calls such as
`initscr()`, `newterm()`, `newwin()`, `subwin()`, `derwin()`, `delwin()`,
`wnoutrefresh()`, and `doupdate()`.

Even here, ncurses documentation is worth reading because it documents real
behavior, error conditions, and extensions more concretely than many older
summaries.

### Wide-Character Interfaces

The wide build expands the API significantly. Expect families such as:
- `get_wch()` and `wget_wch()` for wide input;
- `add_wch()`, `wadd_wch()`, and related output calls;
- `setcchar()` and `getcchar()` for complex character cells;
- wide-character string calls such as `waddnwstr()` and `get_wstr()`.

If your application uses Unicode heavily, anchor your design around the wide
APIs from the start. Retrofitting later is painful.

### Colors And Extended Colors

ncurses supports the usual color calls such as `start_color()` and
`init_pair()`, but newer releases also expose extended-color entry points
such as `init_extended_pair()` and `init_extended_color()`.

Treat these as implementation-specific features. They can be excellent when
you know ncurses is the target, but they are not the same portability story
as the older color-pair interface.

### Input, Keys, And Resize Handling

ncurses extends the base input story with helpers such as `has_key()` and
`define_key()`, and it documents ESC timing and `KEY_*` behavior in detail.

Resize handling is one of the most important extension families:
- `is_term_resized()` checks whether the library's dimensions differ from a
  proposed size;
- `resize_term()` and `resizeterm()` reconcile library state after a resize.

If a full-screen application misbehaves only after terminal resizes, move
these calls near the top of the suspect list.

### Panels, Menus, And Forms

ncurses ships companion libraries rather than burying everything inside one
monolith:
- panels add depth ordering for overlapping windows;
- menus provide structured item navigation;
- forms provide field validation and navigation.

These libraries are still part of normal ncurses-based application design.
Do not overlook them if the program is reimplementing stacking or field
navigation badly by hand.

### Terminfo Tooling

ncurses is also an operational toolkit. The most common command-line tools
are:
- `infocmp` to inspect or compare terminal descriptions;
- `tic` to compile custom terminfo source;
- `toe` to list available entries;
- `tput` for small capability probes.

These tools are often the fastest way to prove that the bug is in the
terminal description rather than in the application.

## Practical Guidance

Gate implementation-specific code with the `NCURSES_VERSION` macro or with
build-system checks instead of assuming every curses implementation behaves
like ncurses.

Choose the wide build deliberately. Mixing narrow-character assumptions with
wide-character libraries leads to subtle bugs in rendering and input.

If linking fails, check library order as well as library selection. Side
libraries such as panels, menus, and forms sit on top of ncurses rather than
replacing it.

## Sharp Edges

A program can be source-compatible with generic curses while still depending
on ncurses behavior in practice. Be honest in documentation and build flags.

Bad terminfo data can make correct code look broken. Always inspect the
active terminal entry before assuming the library or application is wrong.

Resize, mouse, and extended-color behavior are areas where ncurses-specific
details show up quickly. These are common portability fault lines.

## Further Information

- ncurses project page:
  <https://invisible-island.net/ncurses/>
- ncurses FAQ:
  <https://invisible-island.net/ncurses/ncurses.faq.html>
- ncurses Programming HOWTO:
  <https://invisible-island.net/ncurses/NCURSES-Programming-HOWTO.html>
- ncurses `curs_initscr(3x)` manual:
  <https://invisible-island.net/ncurses/man/curs_initscr.3x.html>
- ncurses `curs_getch(3x)` manual:
  <https://invisible-island.net/ncurses/man/curs_getch.3x.html>
- ncurses `curs_add_wch(3x)` manual:
  <https://invisible-island.net/ncurses/man/curs_add_wch.3x.html>
- ncurses `curs_color(3x)` manual:
  <https://invisible-island.net/ncurses/man/curs_color.3x.html>
- ncurses `resizeterm(3x)` manual:
  <https://invisible-island.net/ncurses/man/resizeterm.3x.html>
