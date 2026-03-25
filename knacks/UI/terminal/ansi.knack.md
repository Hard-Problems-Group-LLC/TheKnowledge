# ANSI Terminal Control Sequences

## When To Load This Knack

Load this knack when you need to read, write, or debug raw terminal control
sequences. It is most useful when a program is emitting literal escape
sequences, when terminal output is corrupted, or when you need to decide
whether a behavior belongs to the standardized control language or to a
terminal-specific extension.

## Mental Model

Most terminal control traffic is a byte stream with ordinary printable text
mixed with control bytes and control sequences. In practice, people often say
"ANSI escapes," but modern terminal behavior is a layered mix:
- ASCII and C0 control bytes such as BEL, BS, CR, and LF.
- ECMA-48 or ISO 6429 control functions such as CSI cursor movement, erase
  operations, and SGR text attributes.
- DEC private modes and sequences inherited from VT-series terminals.
- Emulator-specific extensions, especially from xterm and its imitators.

That layering matters. `ESC [ 31 m` is widely portable because it is an
SGR-style sequence from the standard control language. `ESC [ ? 1049 h` is
not portable in the same way because it is a DEC-private or xterm-family
extension used for alternate-screen behavior.

Think of a terminal as a state machine, not as a stateless renderer. Cursor
position, origin mode, autowrap, insert or replace behavior, protected areas,
current rendition attributes, and selected character sets all affect what the
next bytes mean.

## Sequence Structure

The common sequence families are:
- Single-byte C0 controls such as `BEL`, `BS`, `HT`, `LF`, `CR`, and `ESC`.
- `ESC` sequences, where one or more bytes after `ESC` select a function.
- `CSI` sequences, usually written in 7-bit form as `ESC [`.
- `OSC` sequences for operating-system style commands such as window titles.
- `DCS` and related control strings for longer, structured payloads.

Standard documents also define an 8-bit `CSI` control byte. In practice,
7-bit `ESC [` is far more common because it survives older links and tools
better. When you read documentation, treat `CSI` as the abstract control
function and `ESC [` as the common concrete spelling.

Within a `CSI` sequence:
- Parameter bytes are usually digits and semicolons.
- Intermediate bytes are optional and uncommon in day-to-day work.
- The final byte selects the function.

Examples:
- `ESC [ H` or `ESC [ 1 ; 1 H` moves the cursor home.
- `ESC [ 2 J` erases the display.
- `ESC [ 31 m` sets red foreground in the usual SGR palette model.
- `ESC [ 0 m` resets SGR attributes.

## Practical Guidance

Prefer capability libraries when you need portability. If you are writing a
general terminal program, `terminfo` or a screen library such as curses is
usually safer than hand-assembling escapes. Literal escapes are reasonable
when:
- you are writing a small tool for a known terminal family;
- you need a feature with no portable terminfo abstraction; or
- you are debugging a terminal or emulator directly.

Keep the standardized and private layers separate in your head:
- Cursor movement, erasing, and basic rendition are usually safe to discuss
  as ECMA-48 style behavior.
- Alternate screen, mouse tracking, bracketed paste, window-title control,
  and clipboard features usually belong to emulator-specific extensions.

Be conservative with color assumptions. The baseline SGR vocabulary covers
reset, bold, underline, inverse video, and a small palette model. Indexed
256-color and direct-color conventions are widely implemented, but they are
not all part of the same historical standard layer. Check the terminal
description and emulator documentation before assuming support.

## Sharp Edges

Do not equate "ANSI" with "everything terminals do." That shorthand causes
confusion in bug reports and documentation. A lot of interesting behavior is
really DEC or xterm private behavior.

Do not assume every `ESC` sequence is safe to replay blindly. Some sequences
query the terminal, some change modes, and some affect the host environment
indirectly through features such as clipboard integration or title changes.

Do not assume Unicode text eliminates control-sequence concerns. The text
encoding and the control channel coexist. You can have a UTF-8 terminal and
still rely on an ECMA-48-style control stream for movement and styling.

## Debugging Checklist

- Reduce the problem to captured bytes. Distinguish literal `ESC` traffic
  from printable text first.
- Identify whether the sequence is standardized, DEC private, or
  emulator-specific.
- Check whether `$TERM` matches the emulator the program is actually talking
  to.
- If behavior differs across terminals, compare support for the specific mode
  or control family instead of assuming a generic "ANSI" regression.
- When line drawing or glyph selection looks wrong, verify character-set and
  UTF-8 assumptions separately from cursor-control logic.

## Further Information

- ECMA-48, Control Functions for Coded Character Sets:
  <https://www.ecma-international.org/wp-content/uploads/ECMA-48_5th_edition_june_1991.pdf>
- DEC VT100 User Guide, programmer information:
  <https://vt100.net/docs/vt100-ug/chapter3.html>
- DEC VT220 Programmer Reference Manual:
  <https://vt100.net/docs/vt220-rm/contents.html>
- XTerm control sequences:
  <https://invisible-island.net/xterm/ctlseqs/ctlseqs.html>
- VTTEST manual page:
  <https://invisible-island.net/vttest/manpage/vttest.html>
