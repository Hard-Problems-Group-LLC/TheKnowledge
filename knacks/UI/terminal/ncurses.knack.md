# ncurses

## When To Load This Knack

Load this knack when you are working with the ncurses implementation itself,
not just with the generic curses model. This is the right document when build
systems, library variants, extended color support, terminfo tooling, or
implementation-specific behavior matter.

## Related API Knacks

- `ncurses.api.C.knack.md` covers the ncurses C API, wide-character entry
  points, and common extension families.
- `ncurses.api.CPP.knack.md` covers the shipped C++ wrapper headers and class
  families.
- Python callers normally want `curses.api.Python.knack.md`, because CPython's
  `curses` module targets curses on top of ncurses rather than a separate
  `ncurses` Python package.

## Mental Model

ncurses is the dominant freely available curses implementation on Unix-like
systems. It began as a clone of System V curses and grew into a broader
implementation with its own extensions, tooling, and portability work.

Treat ncurses as two things at once:
- a curses-compatible screen library; and
- a terminal-capability ecosystem that includes terminfo data, compiler and
  query tools, test helpers, and implementation-specific extensions.

That second part is why ncurses shows up even when an application does not
link the library directly. Tools such as `tic`, `infocmp`, `tput`, `toe`,
`tack`, and `vttest` often matter when diagnosing terminal behavior.

## What ncurses Adds In Practice

Compared with the abstract curses model, ncurses often adds:
- wide-character support and the `ncursesw` family;
- implementation extensions not covered by X/Open Curses;
- richer terminfo handling;
- extra utility programs and test tools; and
- behavior that is portable across many real systems even when it is not part
  of the strict standard subset.

This is useful, but it creates a portability boundary. If your application
depends on ncurses extensions, say so clearly in the code and build system.
Do not silently treat them as generic curses behavior.

## Practical Guidance

Prefer wide-character aware interfaces unless you have a specific reason to
stay in narrow-character mode. Modern terminal applications usually want
Unicode-capable handling end to end.

Treat `$TERM` and the terminfo database as first-class dependencies. ncurses
can only emit the right control sequences if it has the right capability
description.

Use ncurses tooling deliberately:
- `infocmp` to inspect what the terminal description claims;
- `tic` to compile or install custom terminfo entries;
- `tput` for small capability probes;
- `tack` and `vttest` when deeper terminal validation is needed.

## Sharp Edges

Do not assume ncurses is part of POSIX. The ncurses FAQ is explicit that
X/Open Curses is a different standard lineage, and ncurses also provides many
extensions beyond it.

Do not assume every "curses" implementation behaves like ncurses. BSD,
vendor, and embedded implementations can differ in APIs, extension support,
and terminfo handling.

Do not guess at color support from emulator marketing. Check the terminfo
entry and the ncurses version and feature set you actually built against.

## Debugging Checklist

- Verify which library variant you are linking, including wide-character
  variants where relevant.
- Inspect the active terminfo entry with `infocmp`.
- Reproduce key display issues with ncurses sample tools or terminal tests
  before blaming your application logic.
- Separate X/Open behavior from ncurses-only extensions when judging
  portability.
- If a sequence works in raw tests but fails through ncurses, inspect the
  capability database first.

## Further Information

- ncurses FAQ:
  <https://invisible-island.net/ncurses/ncurses.faq.html>
- ncurses `initscr` manual:
  <https://invisible-island.net/ncurses/man/curs_initscr.3x.html>
- ncurses `getch` manual:
  <https://invisible-island.net/ncurses/man/curs_getch.3x.html>
- ncurses `terminfo` manual:
  <https://invisible-island.net/ncurses/man/terminfo.5.html>
- X/Open `<curses.h>` reference:
  <https://pubs.opengroup.org/onlinepubs/7908799/xcurses/curses.h.html>
- VTTEST project:
  <https://invisible-island.net/vttest/>
