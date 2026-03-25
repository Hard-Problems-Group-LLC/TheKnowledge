# ncurses C++ API

## When To Load This Knack

Load this knack when you are dealing with the C++ wrapper layer shipped by
ncurses itself. This is the right document when the code includes headers
such as `cursesw.h`, `cursesapp.h`, `cursesf.h`, or `cursesm.h`, or when it
links `libncurses++` or `libncurses++w`.

## Relationship To Other Knacks

- `ncurses.knack.md` covers the implementation at the architectural level.
- `ncurses.api.C.knack.md` covers the underlying C entry points that the C++
  wrappers sit on top of.
- Python users generally want `curses.api.Python.knack.md`, because
  CPython does not expose a separate ncurses-native module analogous
  to these C++ headers.

## Mental Model

ncurses ships an older object-oriented wrapper layer rather than inventing a
separate terminal framework. The C++ API is best understood as:
- inline and class wrappers around the C interface;
- application, panel, menu, and form classes that track the underlying C
  objects; and
- exception types and helper classes that package C return codes in a more
  C++-friendly shape.

This layer is real and shipped, but it is much less common than the plain C
API. Expect sparse web documentation and plan to inspect the installed
headers from the exact ncurses release you are targeting.

## Headers And Libraries

The main wrapper headers are:
- `cursesw.h` for core window, pad, color-window, and wrapper glue;
- `cursesapp.h` for `NCursesApplication` and soft-label-key support;
- `cursesp.h` for `NCursesPanel`;
- `cursesm.h` for menu wrappers;
- `cursesf.h` for form wrappers;
- `cursslk.h` and `etip.h` for soft labels and exception types.

On this system the dynamic libraries include both `libncurses++` and
`libncurses++w`. Add the underlying C libraries as needed, such as
`libncursesw`, `libpanelw`, `libmenuw`, and `libformw`.

## API Families

### Core Window Wrappers

`cursesw.h` defines the base class family. The names visible in the shipped
headers include:
- `NCursesWindow` as the core wrapper around `WINDOW *`;
- `NCursesColorWindow` for color-aware window defaults;
- `NCursesPad` and framed-pad helpers for pad-based views.

The wrapper keeps the familiar curses model visible. You still think in
windows, pads, cursor position, and refresh behavior. The benefit is class
structure, overloaded helpers, and exceptions rather than a radically new
design.

### Panels And Stacking

`cursesp.h` provides `NCursesPanel` and related templates for panel-backed
objects. Use this family when the code depends on overlapping windows and
z-order rather than on plain independent windows.

### Application Framework And Soft Labels

`cursesapp.h` defines `NCursesApplication`, which is the most opinionated
part of the wrapper. The intended style is subclass-based:
- override initialization hooks such as `init()` or title-window behavior;
- optionally configure soft-label keys through `Soft_Label_Key_Set`;
- implement `run()` as the application body;
- invoke the application object to enter the main flow.

This is convenient when the existing application already likes framework-
style inheritance. It is a poor fit if you want a minimal wrapper over a C
event loop.

### Forms And Menus

`cursesf.h` wraps the forms library with classes such as `NCursesForm`,
`NCursesFormField`, and `NCursesFieldType`.

`cursesm.h` wraps the menus library with classes such as `NCursesMenu`,
`NCursesMenuItem`, and callback or user-data helpers.

These wrappers track the same conceptual model as the underlying C forms and
menu libraries, but they package it into constructors, methods, inheritance,
and exceptions.

### Exceptions And Error Handling

`etip.h` provides exception types such as `NCursesException`,
`NCursesPanelException`, `NCursesMenuException`, and
`NCursesFormException`.

That makes the wrapper pleasant to read in some cases, but remember that the
real failure semantics still originate in the underlying C library. You are
not escaping curses constraints; you are only changing how they surface.

## Practical Guidance

Inspect the installed headers from the exact target release. The wrapper API
is stable enough to ship, but it is not documented online nearly as richly
as the C interface.

Prefer the plain C API when portability and team familiarity matter more
than wrapper aesthetics. The C++ layer is valuable mostly when you are
already inside a codebase that uses it.

Keep ownership rules in mind. The wrappers manage C objects, but the model is
older C++ rather than modern smart-pointer-heavy design. Read constructors,
destructors, and copy behavior before assuming ordinary value semantics.

## Sharp Edges

Do not treat the wrapper as a modern cross-platform widget framework. It is a
thin OO layer over curses, not a replacement for a contemporary TUI toolkit.

Web references for the C++ layer are sparse. If a class behavior seems odd,
the matching installed header is often the primary source of truth.

Mixing wide and narrow libraries is easy to get wrong. If the build uses the
`w` variants of the C libraries, match them with `libncurses++w` and the
wide-character headers and assumptions.

## Further Information

Official web material for the ncurses C++ wrappers is sparse. Pair these
URLs with the installed headers `cursesw.h`, `cursesapp.h`, `cursesp.h`,
`cursesf.h`, `cursesm.h`, `cursslk.h`, and `etip.h` from the exact release
you are targeting.

- ncurses project page:
  <https://invisible-island.net/ncurses/>
- ncurses release announcement page:
  <https://invisible-island.net/ncurses/announce.html>
- ncurses FAQ:
  <https://invisible-island.net/ncurses/ncurses.faq.html>
- ncurses archives:
  <https://invisible-island.net/archives/ncurses/>
- GNU ncurses release directory:
  <https://ftp.gnu.org/gnu/ncurses/>
