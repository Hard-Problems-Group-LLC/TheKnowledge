# Curses Programming Model

## When To Load This Knack

Load this knack when you are building or debugging a full-screen terminal
application and need the portable curses mental model rather than raw escape-
sequence trivia. It is especially useful when you are choosing between
hand-written terminal control and a screen library, or when a bug might be in
the terminal description rather than in your window-update code.

## Related API Knacks

- `curses.api.C.knack.md` maps the standard C entry points, object model, and
  terminfo-facing calls.
- `curses.api.Python.knack.md` covers Python's `curses` module together with
  `curses.ascii`, `curses.panel`, and `curses.textpad`.

## Mental Model

Curses is a screen-management abstraction for character-cell terminals. The
core idea is simple:
- your application updates an internal model of windows and pads;
- the library compares desired state with terminal state; and
- the library emits the terminal-specific control sequences needed to make the
  display match.

That design lets one program target many terminals without hard-coding their
escape sequences. The portability story depends on terminal capability data,
traditionally from termcap and now more commonly from terminfo.

Think in terms of three layers:
- application intent, such as "draw a border" or "read a function key";
- curses API calls, such as `addstr`, `refresh`, `wgetch`, and `keypad`;
- terminal capabilities and escape sequences selected through the terminal
  database.

If you skip the bottom layer in your reasoning, curses bugs become mysterious.
Many apparent library bugs are really bad `$TERM` values or mismatched
terminfo entries.

## Core Operating Pattern

Initialization and teardown:
- set up the terminal with `initscr` or `newterm`;
- choose input modes such as `cbreak`, `raw`, `echo`, and `keypad`;
- draw into windows or pads; and
- call `refresh` or `doupdate` to flush the virtual screen to the real one.

Input handling:
- `keypad` enables decoding of multibyte key sequences into logical key
  codes.
- Without it, arrow keys and similar input often arrive as raw escape
  sequences.

Output handling:
- curses is optimized around incremental screen updates.
- Repainting the whole screen on every change is possible, but often misses
  the point of the abstraction.

## What Curses Is Good At

- portable full-screen text interfaces;
- safe cursor movement and region updates;
- abstract key decoding through terminal capability data; and
- line-drawing, colors, and text attributes at the level supported by the
  implementation and terminal description.

It is not a magic escape-sequence suppressor. If the terminal description is
wrong, curses can only be portably wrong.

## Sharp Edges

Do not mix large amounts of raw terminal output with curses-managed screen
state unless you deliberately resynchronize. Out-of-band writes confuse the
library's picture of the terminal.

Do not blame curses first when special keys are wrong. Check whether `keypad`
is enabled and whether `$TERM` identifies the terminal correctly.

Do not assume curses standardization is the same as POSIX. The historical and
standards story is separate, and real implementations vary.

Do not ignore teardown. If you leave the terminal in raw or noecho mode after
errors, the program will feel broken even if the screen drawing was fine.

## Debugging Checklist

- Confirm `$TERM` and inspect the loaded terminal description.
- Check whether the program uses `initscr` or `newterm` correctly.
- Check `cbreak`, `raw`, `echo`, `noecho`, and `keypad` settings before
  chasing display bugs.
- Minimize raw writes to stdout or stderr while curses owns the screen.
- If behavior differs across systems, separate curses-standard behavior from
  implementation-specific extensions.

## Further Information

- X/Open `<curses.h>` reference:
  <https://pubs.opengroup.org/onlinepubs/7908799/xcurses/curses.h.html>
- X/Open terminfo reference:
  <https://pubs.opengroup.org/onlinepubs/7908799/xcurses/terminfo.html>
- ncurses `initscr` manual:
  <https://invisible-island.net/ncurses/man/curs_initscr.3x.html>
- ncurses `terminfo` manual:
  <https://invisible-island.net/ncurses/man/terminfo.5.html>
- ncurses FAQ:
  <https://invisible-island.net/ncurses/ncurses.faq.html>
