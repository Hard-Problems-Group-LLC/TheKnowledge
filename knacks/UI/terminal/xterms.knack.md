# XTerm-Family Emulators

## When To Load This Knack

Load this knack when you are working with a modern terminal emulator that
tracks xterm behavior directly or loosely. This is the right document when
you need to reason about alternate screens, mouse tracking, bracketed paste,
window-title sequences, focus events, or why an emulator that claims to be
"xterm-compatible" still behaves differently from real xterm.

## Mental Model

XTerm is both a concrete program and the reference implementation for a large
set of modern terminal-emulator conventions. A lot of terminal features that
people now think of as generic are really xterm-era conventions built on top
of older DEC behavior.

In practice, the xterm layer combines:
- VT100 and VT220 style control semantics;
- emulator-private control sequences and modes;
- terminfo or termcap descriptions used by applications;
- X11-era resource configuration; and
- modern usability features such as clipboard helpers, mouse protocols, and
  UTF-8 aware rendering.

That means "xterm-compatible" is never binary. Some emulators copy title
setting but not mouse reporting. Some copy alternate-screen behavior but use a
different terminfo story. Some accept the same escape sequences but differ in
scrollback, resize behavior, or clipboard security policy.

## Features That Usually Matter

Alternate screen:
- XTerm keeps normal and alternate screen buffers separate.
- Applications such as editors and pagers commonly switch with private modes
  such as `1047`, `1048`, or `1049`.
- The alternate screen normally has no scrollback history.

Bracketed paste:
- Private mode `2004` wraps pasted text so programs can distinguish paste
  input from typing.
- Shells, line editors, and full-screen tools rely on this to avoid accidental
  command execution or broken indentation behavior.

Mouse and focus reporting:
- XTerm defines several mouse modes, including button tracking and SGR mouse
  encoding.
- Full-screen applications often enable these dynamically, so mouse bugs may
  be mode-negotiation bugs rather than raw input bugs.
- Focus in and focus out events are also optional negotiated behavior.

Operating-system commands:
- `OSC` sequences are commonly used for window titles and similar metadata.
- Some emulators also implement clipboard features and hyperlinks here.
- Treat these as powerful, non-portable features rather than as harmless text
  styling.

## Terminfo Matters

Applications should not guess xterm behavior from the emulator window title.
They should use the terminal description selected by `$TERM`. This is where a
lot of avoidable bugs come from.

Important rules:
- Prefer a terminfo entry that matches the emulator's real capability set.
- Do not force `xterm-color` or another older entry just because it "usually
  works."
- When an application uses curses or terminfo, a bad terminal description can
  make correct escape-sequence support look broken.

The xterm FAQ explicitly calls out the terminfo and termcap files shipped with
xterm and warns against loose `$TERM` habits. Treat that as operational
guidance, not trivia.

## Sharp Edges

Do not assume every terminal that supports xterm title changes also supports
xterm mouse, focus, clipboard, or alternate-screen behavior in the same way.

Do not assume scrollback behavior is standardized. The alternate-screen split,
the effect of private modes, and resource knobs such as `titeInhibit` can all
change what users perceive.

Do not treat xterm extensions as safe by default in hostile or mixed-trust
environments. Title changes, clipboard integration, and other operating-
system-style commands may have security or operator-experience implications.

## Debugging Checklist

- Check the actual emulator, not just its profile name.
- Check `$TERM` and the loaded terminfo entry.
- Identify the exact private mode or control family in play.
- Reproduce with xterm itself if you need a reference implementation.
- Use `vttest` for display and keyboard baselines, then compare emulator-
  specific behavior separately.

## Further Information

- XTerm FAQ:
  <https://invisible-island.net/xterm/xterm.faq.html>
- XTerm control sequences:
  <https://invisible-island.net/xterm/ctlseqs/ctlseqs.html>
- XTerm control-sequence documents:
  <https://invisible-island.net/xterm/ctlseqs/>
- VTTEST project:
  <https://invisible-island.net/vttest/>
- VTTEST manual page:
  <https://invisible-island.net/vttest/manpage/vttest.html>
- DEC VT220 Programmer Reference Manual:
  <https://vt100.net/docs/vt220-rm/contents.html>
