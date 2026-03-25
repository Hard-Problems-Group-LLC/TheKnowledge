# Bubblewrap

Load this knack when a tool, test harness, or agent runtime uses Linux
namespace sandboxing and you need to know what bubblewrap is doing and why it
is failing. Bubblewrap is a low-level Linux sandbox builder used by Flatpak
and similar tooling. It is much closer to "assemble exactly the namespace and
filesystem view I want" than to "run a general-purpose container platform for
me."

## Mental Model

Bubblewrap starts by creating a new filesystem namespace whose root is a fresh
tmpfs. Nothing from the host is visible inside that root until you bind it in.
That one fact explains most behavior:

- If a binary, library, config file, or device is missing inside the sandbox,
  bubblewrap was not told to expose it.
- If a path should be visible but read-only, use `--ro-bind` instead of
  `--bind`.
- If a writable area should be ephemeral, prefer `--tmpfs` or
  `--tmp-overlay` instead of binding a host directory read-write.

Bubblewrap can also create new Linux namespaces for users, processes, IPC,
networking, UTS, and cgroups. The sandbox shape is therefore the product of
two things:

1. The filesystem tree you assemble with bind, tmpfs, proc, dev, and overlay
   operations.
2. The kernel-isolation features you enable or retain with the namespace
   flags.

Think of bubblewrap as a deterministic sandbox constructor. The command line
is the contract.

## Common Building Blocks

These flags do most of the day-to-day work:

- `--ro-bind SRC DEST`: expose a host path read-only.
- `--bind SRC DEST`: expose a host path read-write.
- `--proc /proc` and `--dev /dev`: create basic process and device views.
- `--tmpfs DEST`: give the sandbox an empty writable tmpfs.
- `--dir DEST`: create a directory inside the synthetic root.
- `--chdir DIR`: set the child process working directory.
- `--setenv VAR VALUE` and `--unsetenv VAR`: control environment leakage.
- `--unshare-user`, `--unshare-pid`, `--unshare-net`, and friends: create
  additional kernel namespace boundaries.
- `--unshare-all`: start from the strict side, then selectively relax with
  flags such as `--share-net`.
- `--new-session`: detach from the controlling terminal with `setsid()`.
- `--die-with-parent`: kill the sandbox tree if the parent process dies.

`--new-session` matters more than it first appears to. The bubblewrap manual
notes that, in a general sandbox, omitting it means you should also use
seccomp to block `TIOCSTI`; otherwise, a sandboxed process may be able to
inject terminal input back into the parent session.

## Practical Patterns

### Read-Mostly Command Sandbox

Use this shape when a command should see normal system binaries and libraries,
but the current working tree should stay untouched unless you explicitly bind
something writable:

```bash
bwrap \
  --unshare-all \
  --share-net \
  --ro-bind /usr /usr \
  --ro-bind /bin /bin \
  --ro-bind /lib /lib \
  --ro-bind /lib64 /lib64 \
  --ro-bind /etc /etc \
  --proc /proc \
  --dev /dev \
  --tmpfs /tmp \
  --dir /work \
  --ro-bind "$PWD" /work \
  --chdir /work \
  --new-session \
  --die-with-parent \
  sh
```

If the host uses `/sbin`, `/usr/lib64`, or other distro-specific paths,
remember to bind those too. Bubblewrap will not infer them.

### Writable Workspace With Explicit Blast Radius

If the sandbox must write back into the current tree, make that decision
deliberately and keep the writable mount narrow:

```bash
bwrap \
  --unshare-all \
  --share-net \
  --ro-bind /usr /usr \
  --ro-bind /bin /bin \
  --ro-bind /lib /lib \
  --ro-bind /lib64 /lib64 \
  --proc /proc \
  --dev /dev \
  --tmpfs /tmp \
  --dir /work \
  --bind "$PWD/subdir" /work \
  --chdir /work \
  --new-session \
  --die-with-parent \
  make test
```

That pattern is safer than binding the whole repository writable.

### Agent And Tool Sandboxes

Agent runtimes often wrap shell commands with bubblewrap rather than asking
operators to write raw `bwrap` invocations. In that situation, treat the
bubblewrap command line as generated infrastructure, but debug it the same
way:

1. Check `bwrap --help` or `bwrap --version`.
2. Compare the installed feature set with what the wrapper expects.
3. Distinguish "bubblewrap is too old" from "the outer environment forbids
   nested sandboxing."
4. Reproduce with the runtime's dedicated sandbox subcommand if it has one.

A wrapper may successfully detect one compatibility problem and still fail
later because a container, VM, or outer sandbox blocks namespace setup that
would succeed on a normal host shell.

## High-Value Troubleshooting

### `bwrap: Unknown option --argv0`

This is a version-skew problem. The local tool is asking bubblewrap to set the
child's `argv[0]`, but the installed `bwrap` build does not support that
flag. In March 2026, `openai/codex` tracked exactly this failure on Ubuntu
20.04.6 LTS, whose packaged `bubblewrap 0.4.0` did not list `--argv0` in
`bwrap --help`.

Debug checklist:

- Run `bwrap --help` and confirm whether `--argv0` appears.
- Run `bwrap --version` and compare it with the minimum expected by the
  calling tool.
- Check whether the wrapper can fall back to a vendored bubblewrap build.
- If the distro package is pinned to an older series, a system update
  may not be enough.

For Codex specifically, `openai/codex` merged a March 2026 fix to fall back
to a vendored bubblewrap when the system `bwrap` lacks `--argv0`. That is a
wrapper-level mitigation, not a guarantee that every other bubblewrap consumer
will do the same.

### `Operation not permitted`

This message is broad. The usual causes are:

- unprivileged user namespaces are disabled;
- the host kernel or container policy forbids creating the requested
  namespace;
- the setuid versus non-setuid build changes which options are legal; or
- an outer sandbox is preventing a nested sandbox from opening the resources
  bubblewrap needs.

Narrow it down by removing optional namespace flags one at a time. If
`--unshare-net` is the first failing piece, the real issue is often the
environment's networking-namespace policy rather than the filesystem setup.

### `loopback: Failed to create NETLINK_ROUTE socket: Operation not permitted`

This usually means the process is trying to manage network-namespace state in
an environment that forbids it. A practical reading is: "bubblewrap itself is
present, but the outer sandbox or container will not let it complete network
setup."

That is not the same failure as an old `bwrap` binary missing a flag. If a
wrapper first reports that it is using a compatible or vendored bubblewrap and
later fails here, the version check already succeeded and the remaining issue
is nested-sandbox capability.

### Missing Files Or Immediate `ENOENT`

When a program fails immediately with "file not found" inside bubblewrap, do
not jump straight to permissions. First confirm that every required path was
bound into the synthetic root and that `--chdir` points to an existing
destination inside that root. Bubblewrap only shows what you mounted.

### Setuid Caveats

Some bubblewrap features are unavailable in the setuid build. The official
manual explicitly calls out several examples, including `--disable-userns`,
`--userns`, and overlay-related options. If a command works on one machine and
fails on another, compare not only the bubblewrap version but also whether the
installed build is setuid-root or fully unprivileged.

## Working Habits That Pay Off

- Prefer the smallest writable surface that still lets the task complete.
- Use `--new-session` and `--die-with-parent` by default for interactive tool
  wrappers unless you have a reason not to.
- Treat `--unshare-all` plus explicit opt-backs-in as the clearest starting
  posture for new sandboxes.
- Reproduce wrapper failures with a minimal direct `bwrap` command whenever
  you need to separate bubblewrap mechanics from wrapper bugs.
- Keep one eye on the outer environment. Containers, CI sandboxes, and agent
  sandboxes can all make a perfectly valid bubblewrap command fail for reasons
  unrelated to the command itself.

## Further Information

- Bubblewrap project repository:
  <https://github.com/containers/bubblewrap>
- Bubblewrap reference manual (`bwrap.xml`):
  <https://github.com/containers/bubblewrap/blob/main/bwrap.xml>
- Bubblewrap releases:
  <https://github.com/containers/bubblewrap/releases>
- Bubblewrap 0.9.0 release notes:
  <https://github.com/containers/bubblewrap/releases/tag/v0.9.0>
- Codex issue `#15283` on missing `--argv0` support:
  <https://github.com/openai/codex/issues/15283>
- Codex PR `#15338` for vendored-bubblewrap fallback:
  <https://github.com/openai/codex/pull/15338>
