# GitHub SSH And Git Identity In A Multi-Organization Consulting Workflow

This document is a practical and conceptual guide to a problem that shows up constantly for consultants, employees working across multiple legal entities, and anyone who moves between personal, client, and employer-owned repositories on the same machine: how to make SSH authentication, Git commit identity, and GitHub attribution all line up reliably without leaking the wrong email address or using the wrong account.

The short version is simple:

- SSH keys decide how you authenticate to GitHub.
- Git config decides what name and email get written into commits.
- GitHub decides whether those commit emails map back to one of your accounts.

Those are three different mechanisms. Many messy setups fail because they assume they are one mechanism.

The examples in this document are intentionally pseudonymous so the guidance can be shared publicly. The example user is `Jane Doe`, with the short username `jdoe`, and the example organizations are a mix of hacker-culture and cyberpunk-fiction names: `Fuchi`, `Cross`, `Booji Boy Heavy Industries, Ltd.`, and `Yoyodyne`.

The example email domains use `.example`, which is reserved for documentation and examples. That is deliberate. It keeps the document safe to reuse without accidentally pointing at real organizations.

## Executive Summary

The working pattern on this machine is:

- one SSH alias per organization in `~/.ssh/config`
- one SSH key per organization
- one org root under `~/codebase` per organization
- one per-org Git include file with the correct `user.email`
- `user.useConfigOnly = true` globally, so Git does not invent fallback identities
- `includeIf` rules keyed primarily off repo path and secondarily off remote URL alias

Current intended mapping in the example configuration:

- `github-fuchi` -> `Jane Doe <jdoe@fuchi.example>`
- `github-cross` -> `Jane Doe <jdoe@cross.example>`
- `github-boojiboy` -> `Jane Doe <jdoe@boojiboy.example>`
- `github-yoyodyne` -> `Jane Doe <jdoe@yoyodyne.example>`

Current org directory convention in the example configuration:

- `~/codebase/Fuchi/actual/...`
- `~/codebase/Cross/actual/...`
- `~/codebase/BoojiBoy/actual/...`
- `~/codebase/Yoyodyne/actual/...`
- `~/codebase/Fuchi/<ClientName>/...`
- `~/codebase/Cross/<ClientName>/...`
- `~/codebase/BoojiBoy/<ClientName>/...`
- `~/codebase/Yoyodyne/<ClientName>/...`

Under each org root, `actual/` means first-party work for that organization itself: internal tooling, internal infrastructure, products or libraries the organization owns, and other repositories where the organization is the principal actor rather than a vendor. Client work should live in sibling directories next to `actual/`, one directory per client.

That distinction is not merely cosmetic. It is a compact way of encoding who the work is for, who is expected to own or control the resulting IP in the ordinary case, and which email/account defaults should apply. It is policy shorthand, not a substitute for actual contract language, but it is useful shorthand.

That pattern is strong enough for day-to-day use and understandable enough that it can be debugged later without guesswork.

## The Real Problem

The administrative headache here is not merely "how do I use multiple SSH keys?" The deeper problem is that "identity" in Git/GitHub work has several layers that people casually collapse together.

The layers are:

1. Transport authentication.
This is how your machine proves to GitHub that it is allowed to access a repository. With SSH, this is controlled by the private key offered to the server.

2. Commit metadata.
This is what gets baked into each commit object as author and committer name/email. Git's own documentation states that `user.name` and `user.email` determine what ends up in the author and committer fields, unless overridden by more specific settings or environment variables. Git also documents that `GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_NAME`, `GIT_COMMITTER_EMAIL`, and even `EMAIL` can override config values. Source: [git-config documentation](https://git-scm.com/docs/git-config.html).

3. GitHub attribution.
GitHub uses the commit email address to associate commits with your account. GitHub also notes that to have commits attributed to you and counted in your contributions graph, the email must be connected to your account, or you must use GitHub's provided `noreply` address. Source: [GitHub email addresses docs](https://docs.github.com/en/account-and-profile/concepts/email-addresses).

4. Authorization and organization policy.
Even if authentication and attribution are correct, repository access still depends on the right account being a member of the right org, team, or repo. In some environments, this also intersects with SSO or enterprise account policy.

These layers are independent enough that it is entirely possible to:

- authenticate as one account
- create commits with a different email
- have GitHub attribute those commits to a third account or to no account at all

That is exactly the kind of subtle failure mode that produces embarrassing public metadata, broken contribution graphs, or "why did GitHub think this work came from the wrong identity?" confusion.

## Why Naive Setups Break

The default Git experience is optimized for someone with one identity on one machine, not for a consultant juggling multiple organizations.

The common naive patterns are:

- one global `user.email` for everything
- one SSH key loaded into the agent for everything
- cloning repos anywhere on disk with no path convention
- assuming the GitHub account used for SSH controls commit email
- assuming `git config --global` always writes to the "real" global config

Those assumptions fail in predictable ways.

### Failure mode 1: a single global `user.email`

This is the most common and the most dangerous. A person sets a perfectly reasonable global identity for one employer or one personal account, then later clones a repo for another org and starts committing. Nothing in the default setup forces them to notice that the commit email is wrong.

Git's own answer to this is not "be more careful." Git provides configuration scopes and conditional includes specifically so that different repositories can resolve to different identities. Git also provides `user.useConfigOnly`, which tells Git not to guess default values for name and email. Git's docs explicitly say this is useful when you have multiple email addresses and want different ones for different repositories. Source: [git-config documentation](https://git-scm.com/docs/git-config.html).

### Failure mode 2: multiple SSH keys in the agent, wrong key offered

GitHub's docs on managing multiple accounts show the standard pattern: distinct SSH host aliases in `~/.ssh/config`, each with a specific `IdentityFile`, and `IdentitiesOnly yes`. GitHub explicitly notes that `IdentitiesOnly` ensures SSH uses the correct key when multiple keys are loaded. Source: [GitHub docs on managing multiple accounts](https://docs.github.com/en/account-and-profile/how-tos/account-management/managing-multiple-accounts).

Without that, the wrong key can be tried first, and the result may be confusing:

- permission denied
- authentication as the wrong account
- intermittent behavior that depends on which keys the agent has loaded today

### Failure mode 3: machine-generated fallback identities

Git will try to guess name/email defaults if you let it. On a single-user hobby machine, that can be harmless. In a multi-org environment, it is a foot-gun. This machine already produced an example of the risk: a commit ended up with an email derived from a Tailscale domain. That was not the intended public identity for the repository.

This is exactly why `user.useConfigOnly = true` is valuable. It turns a silent metadata leak into a visible setup error.

### Failure mode 4: tooling that overrides `HOME`

One subtle issue encountered here is that some tools run with an isolated or synthetic `HOME`. That means:

- `git config --global` may write to an alternate `.gitconfig`
- `~/.ssh/config` may resolve to the wrong home directory
- a script that "looks correct" may be editing the wrong user's config

Git documents that the global config is read from `$XDG_CONFIG_HOME/git/config` and `~/.gitconfig`, with `~` resolved from `HOME`. Source: [git-config documentation](https://git-scm.com/docs/git-config.html). In practice, if `HOME` is being overridden, "global" may not mean what an operator thinks it means.

For multi-tool or AI-assisted environments, this matters a lot.

### Failure mode 5: web UI commits and command-line commits use different knobs

GitHub's docs distinguish between:

- commits pushed from the command line, where you set the email in Git
- web-based Git operations, where GitHub uses the email preferences in your GitHub account

That means a person can have their command-line identity configured correctly and still produce different commit metadata in the GitHub web UI if their GitHub email/privacy settings differ. Source: [GitHub email docs](https://docs.github.com/en/account-and-profile/concepts/email-addresses).

## The Design Principles Behind The Current Setup

The current setup is opinionated. That is intentional. Good identity hygiene tends to come from limiting ambiguity, not from maximizing cleverness.

The guiding principles are:

- make the correct behavior the default
- make the wrong behavior noisy
- make repo placement semantically meaningful
- keep SSH auth and Git identity separate but aligned
- use stable, human-readable alias names
- favor simple inspection commands over magical automation

That yields four concrete design choices.

### 1. One SSH alias per org

Each organization gets its own `Host` block in `~/.ssh/config`, all pointing at `github.com` but with different key files:

```sshconfig
Host github-fuchi
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_Fuchi_jdoe_cyberdeck_27MAR2026
    IdentitiesOnly yes

Host github-cross
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_Cross_jdoe_cyberdeck_27MAR2026
    IdentitiesOnly yes

Host github-boojiboy
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_BoojiBoy_jdoe_cyberdeck_27MAR2026
    IdentitiesOnly yes

Host github-yoyodyne
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_Yoyodyne_jdoe_cyberdeck_27MAR2026
    IdentitiesOnly yes
```

The alias names are lowercase and descriptive. That matters more than it sounds. Host aliases turn into muscle memory and remote URLs, so consistency is operationally useful.

### 2. One org root under `~/codebase`

This example setup assumes:

- `~/codebase/Fuchi/`
- `~/codebase/Cross/`
- `~/codebase/BoojiBoy/`
- `~/codebase/Yoyodyne/`

Within each org root:

- `actual/` is first-party work for the org itself
- future client work belongs in sibling directories, one directory per outside client

This is not just filing discipline. It is part of the identity system, because Git can use path-based conditional includes.

### 2a. What `actual/` means and what it does not mean

This directory naming convention deserves explicit treatment because it is doing two jobs at once:

- it is organizing repositories for humans
- it is acting as an input to Git identity policy

The intended meaning is:

- `~/codebase/Fuchi/actual/...` means work done on behalf of Fuchi itself
- `~/codebase/Fuchi/AcmeBank/...` means work Fuchi is doing for AcmeBank as a client

That usually tracks an ownership and governance distinction:

- `actual/` generally implies first-party or organization-owned work
- client peer directories generally imply work performed for an outside client, where ownership, control, confidentiality, or approval rights may differ

But the filesystem is only a policy signal, not a legal instrument. A repository living under `actual/` is not magically transformed into org-owned IP if the contract says otherwise, and a repository under a client directory does not eliminate the need for proper contractual assignments, confidentiality handling, or access review.

What the directory convention does provide is an operationally useful default:

- operators can usually infer which identity should be used
- humans can usually infer why a repo lives where it does
- automation can key off the path structure without needing to understand every contract

In this model, the Git identity follows the organization root, not the subdirectory below it. That means `~/codebase/Fuchi/actual/...` and `~/codebase/Fuchi/AcmeBank/...` both inherit the Fuchi identity. If a workflow requires different commit identities per client, that is a different policy choice and should be modeled explicitly rather than assumed.

In practice, that is exactly the level of precision a working engineering policy needs.

### 2b. Worked example

Suppose Jane Doe works for Fuchi and has two repositories on the same machine:

- `~/codebase/Fuchi/actual/widgetlib`
- `~/codebase/Fuchi/AcmeBank/payment-gateway`

In this policy model:

- both repositories use the Fuchi SSH alias when talking to GitHub
- both repositories resolve to the Fuchi Git identity
- the first path tells humans and automation that `widgetlib` is first-party Fuchi work
- the second path tells humans and automation that `payment-gateway` is client work being done by Fuchi for AcmeBank

That means the expected effective identity in both repositories is:

```text
Jane Doe <jdoe@fuchi.example>
```

The path does not change the commit identity. The path changes the meaning of the engagement.

This matters because the questions "who is doing the work?" and "who is the work for?" are related but not identical:

- the Git identity answers who is doing the work
- the directory location answers who the work is for

That is the core conceptual move in this policy.

### 3. Path-based Git identity overrides

Git supports `includeIf` rules with `gitdir:` patterns. The official docs say that if the `.git` directory location matches the pattern, the condition is met and the included config is loaded. Source: [git-config conditional includes](https://git-scm.com/docs/git-config.html).

That leads to a clean setup in `~/.gitconfig`:

```ini
[core]
    editor = vim

[user]
    name = Jane Doe
    email = jdoe@fuchi.example
    useConfigOnly = true

[includeIf "gitdir:/home/jdoe/codebase/Fuchi/"]
    path = ~/.gitconfig-fuchi

[includeIf "gitdir:/home/jdoe/codebase/Cross/"]
    path = ~/.gitconfig-cross

[includeIf "gitdir:/home/jdoe/codebase/BoojiBoy/"]
    path = ~/.gitconfig-boojiboy

[includeIf "gitdir:/home/jdoe/codebase/Yoyodyne/"]
    path = ~/.gitconfig-yoyodyne

[includeIf "hasconfig:remote.*.url:git@github-fuchi:**"]
    path = ~/.gitconfig-fuchi

[includeIf "hasconfig:remote.*.url:git@github-cross:**"]
    path = ~/.gitconfig-cross

[includeIf "hasconfig:remote.*.url:git@github-boojiboy:**"]
    path = ~/.gitconfig-boojiboy

[includeIf "hasconfig:remote.*.url:git@github-yoyodyne:**"]
    path = ~/.gitconfig-yoyodyne
```

Each included file contains only the per-org identity:

```ini
[user]
    name = Jane Doe
    email = jdoe@cross.example
```

and similarly for the other orgs.

The primary mechanism here is the `gitdir:` rule. The `hasconfig:remote.*.url:` rule is secondary. Git documents that `hasconfig:remote.*.url` scans for matching remote URLs and can conditionally include config based on them, but also notes that included files loaded by that mechanism cannot themselves contain remote URLs. Source: [git-config hasconfig condition](https://git-scm.com/docs/git-config.html).

In practice:

- path-based includes are deterministic and should do most of the work
- remote-based includes are useful as a backstop

### 4. `useConfigOnly = true`

This is the guardrail that turns a hidden error into an explicit one.

If a repo lands outside the expected directory tree, or the include rules do not match, Git should not quietly invent an email from hostnames, account names, or environment guesses. It should fail until the operator fixes the identity.

For multi-org work, that is the right bias.

## Reference Implementation On This Machine

In a real deployment, the relevant files are:

- `~/.ssh/config`
- `~/.gitconfig`
- `~/.gitconfig-fuchi`
- `~/.gitconfig-cross`
- `~/.gitconfig-boojiboy`
- `~/.gitconfig-yoyodyne`

The org layout docs in one plausible deployment would live at:

- `~/codebase/README.md`
- `~/codebase/Fuchi/README.md`
- `~/codebase/Cross/README.md`
- `~/codebase/BoojiBoy/README.md`
- `~/codebase/Yoyodyne/README.md`

In many real rollouts:

- one organization may already have active repositories
- other org roots may exist before their first repos are cloned
- some non-default SSH keys may not yet be registered with GitHub
- some org roots may not yet contain real repositories

That is acceptable. Authentication readiness and local identity routing are related but not identical concerns.

## Replicating This On Another Machine

The order matters.

### Step 1: create or copy the SSH keys

Place one private/public keypair per org in `~/.ssh/`. The filenames do not need to match this machine exactly, but the aliases in `~/.ssh/config` must point at the right files.

For a fresh setup, use `ed25519` keys. A practical naming pattern similar to
one real-world local convention is:

- `id_<Org>_<shortname>_<machine-or-context>_<DATE>`
- matching `.pub` files beside the private keys
- a comment equal to the org-specific email, such as `jdoe@fuchi.example`

Using the pseudonymous identities from this document, one reasonable set of
commands would be:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_Fuchi_jdoe_cyberdeck_27MAR2026 -C jdoe@fuchi.example
ssh-keygen -t ed25519 -f ~/.ssh/id_Cross_jdoe_cyberdeck_27MAR2026 -C jdoe@cross.example
ssh-keygen -t ed25519 -f ~/.ssh/id_BoojiBoy_jdoe_cyberdeck_27MAR2026 -C jdoe@boojiboy.example
ssh-keygen -t ed25519 -f ~/.ssh/id_Yoyodyne_jdoe_cyberdeck_27MAR2026 -C jdoe@yoyodyne.example
```

That yields filenames that stay readable at a glance:

- org name is obvious
- the short user token stays consistent
- the machine or context token explains where the key originated
- the date reduces ambiguity when keys are rotated or replaced later

### Step 2: write `~/.ssh/config`

Add one `Host` alias per org, all pointing at `github.com`, with `IdentitiesOnly yes`.

### Step 3: register the public keys with GitHub

GitHub's SSH docs are clear: after generating a keypair, you must add the public key to the relevant GitHub account to use it for authentication. Source: [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

If this step is missing, local config can still look fine, but `ssh -T` or `git push` will fail.

### Step 4: create the org directory roots

Create:

- `~/codebase/Fuchi/actual`
- `~/codebase/Cross/actual`
- `~/codebase/BoojiBoy/actual`
- `~/codebase/Yoyodyne/actual`

Then, as client work appears, create peer directories such as:

- `~/codebase/Fuchi/AcmeBank`
- `~/codebase/Cross/CityTransit`
- `~/codebase/BoojiBoy/OmniConsumer`

If your naming differs on another machine, update the `gitdir:` paths in `~/.gitconfig` accordingly.

### Step 5: write `~/.gitconfig` and include files

Set:

- a sane global default identity
- `useConfigOnly = true`
- one include file per org
- `includeIf` rules based on path
- optional `hasconfig` rules based on remote alias

### Step 6: clone repos into the correct org tree

Examples:

```bash
git clone git@github-fuchi:Fuchi/repo.git ~/codebase/Fuchi/actual/repo
git clone git@github-cross:Cross/repo.git ~/codebase/Cross/actual/repo
git clone git@github-boojiboy:BoojiBoy/repo.git ~/codebase/BoojiBoy/actual/repo
git clone git@github-yoyodyne:Yoyodyne/repo.git ~/codebase/Yoyodyne/actual/repo
```

For client work, the same org identity usually still applies, but the repository lives under the client peer directory instead of `actual/`:

```bash
git clone git@github-fuchi:Fuchi/client-repo.git ~/codebase/Fuchi/AcmeBank/client-repo
git clone git@github-cross:Cross/client-repo.git ~/codebase/Cross/CityTransit/client-repo
```

This aligns both halves of the system:

- SSH uses the org-specific key
- Git sees the org-specific path and selects the org-specific email

It also preserves an important non-technical distinction:

- the Git identity follows the organization performing the work
- the directory location preserves whether the work is first-party (`actual/`) or client-facing (client peer directory)

## Verification Routine

The most useful habit is to verify identity before the first commit, not after the first push.

Run these inside a repo:

```bash
git remote -v
git config user.name
git config user.email
git config --show-origin --get user.email
git config --list --show-origin
```

Run these for SSH:

```bash
ssh -G github-fuchi | rg 'hostname|user|identityfile'
ssh -G github-cross | rg 'hostname|user|identityfile'
ssh -G github-boojiboy | rg 'hostname|user|identityfile'
ssh -G github-yoyodyne | rg 'hostname|user|identityfile'
```

GitHub's testing docs also show the standard connectivity test with `ssh -T git@github.com`; with aliases, the equivalent pattern is `ssh -T git@github-fuchi`, `ssh -T git@github-cross`, and so on. Source: [Testing your SSH connection](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection).

The operator should be able to answer four questions before pushing:

- Which GitHub account/key will SSH use?
- Which email will Git write into commits?
- Is that email attached to the intended GitHub account?
- Is this repo in the right org path?

If any of those answers is fuzzy, the setup is not ready.

## Quick Troubleshooting Checklist

When a repo is using the wrong identity, check these in order:

1. Is the repo under the expected org root?
If a repo that should be under `~/codebase/Fuchi/...` is actually living under `~/src/misc/...`, the path-based include will not trigger.

2. Does the repo have a local override?
Run:

```bash
git config --show-origin --get user.email
git config --show-origin --get user.name
```

If those resolve to `.git/config`, the repository itself may be overriding the intended per-org include.

3. Is the remote URL using the expected SSH alias?
Run:

```bash
git remote -v
```

If the path-based include is not active, a correct alias in `origin` may still save you if the `hasconfig:remote.*.url:` rule matches.

4. Is `HOME` what you think it is?
Run:

```bash
echo "$HOME"
git config --global --list --show-origin
```

If automation or a dev tool is overriding `HOME`, your "global" config may not be the one you expect.

5. Are environment variables overriding Git?
Run:

```bash
env | rg '^(GIT_|EMAIL=)'
```

If `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_EMAIL`, or `EMAIL` are set, they may beat config.

6. Is SSH choosing the wrong key?
Run:

```bash
ssh -G github-fuchi | rg 'hostname|user|identityfile'
```

That will show which key SSH intends to use for the alias.

## Important Edge Cases

### Environment variables can override config

Git documents that author/committer environment variables override config. That means shell wrappers, CI jobs, release tooling, or local scripts can silently replace the expected identity. Source: [git-config documentation](https://git-scm.com/docs/git-config.html).

When debugging a mismatch, check:

```bash
env | rg '^(GIT_|EMAIL=)'
```

### Repo-local config can shadow global includes

A repo may have its own `.git/config` with a local `user.email`. That is legitimate, but it can also conceal a bad clone path or stale identity. `git config --list --show-origin` is the fastest way to see who is winning precedence.

### Author and committer are not always the same

This is easy to miss. A commit has both author metadata and committer metadata. In ordinary local work they are often the same, but they can diverge in rebases, cherry-picks, patch-application flows, automation, or history rewrites.

If you are fixing a bad identity leak or validating a rewrite, check both fields, not just one. A cleanup is incomplete if the bad email still survives in either author or committer metadata.

### Web UI commits are separate

GitHub's docs note that command-line commits use the email configured in Git, while web-based operations use GitHub-side email settings. Source: [GitHub email docs](https://docs.github.com/en/account-and-profile/concepts/email-addresses).

If you care about strict per-org identity hygiene, do not assume the browser will match the shell. Verify GitHub account email/privacy settings too.

### `noreply` is a legitimate alternate policy

Some teams may decide that the right answer is not organization-specific commit emails at all, but GitHub-managed `noreply` addresses tied to the relevant account. GitHub documents that `noreply` addresses can still be used for attribution. Source: [GitHub email docs](https://docs.github.com/en/account-and-profile/concepts/email-addresses).

That is a different policy model, with different tradeoffs:

- it reduces exposure of real email addresses
- it may simplify public contribution attribution
- it may make organizational provenance less obvious from raw commit metadata

This document assumes an organization-email model because that is usually easier to audit in consulting and multi-org employment contexts, but `noreply` is a valid alternative if privacy or account-centric attribution is the stronger requirement.

### One GitHub account vs multiple GitHub accounts

GitHub allows multiple email addresses on one account. That means one workable model is:

- one GitHub account
- several verified org-specific emails
- different commit emails per repo

Another workable model is:

- separate GitHub accounts or enterprise-managed identities
- separate SSH keys
- separate commit emails

Both can work. The config pattern in this document supports either. The important thing is consistency and verification.

## What To Do When The Wrong Identity Already Landed In History

This matters because mistakes will happen.

If the bad identity is only in the most recent local commit, `git commit --amend` is usually enough.

If the bad identity has already been pushed, a limited rewrite may still be manageable:

- amend or rebase locally
- verify the rewritten author/committer metadata
- push with `--force-with-lease`

For larger or more sensitive exposures, GitHub's guidance on history rewriting is worth reading carefully. GitHub warns that rewriting history has side effects, including risk of recontamination from old clones, risk of losing collaborators' work, and changed commit hashes that can break tooling or references. Source: [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

This is especially relevant if the leaked value is:

- a secret
- a private hostname
- an internal domain
- an identity that should not appear in a public repo

The policy implication is simple: prevention is much cheaper than cleanup.

## When This Model Is Wrong

This model is intentionally organization-centric. It works well when:

- one human works across multiple organizations
- each organization wants its own stable SSH key and commit identity
- client work is still being performed under the consultant or employer organization's engineering identity

This model is the wrong default when:

- a client requires commits to come from client-owned GitHub identities
- a client requires use of client-managed SSH keys or enterprise-managed users
- work must be isolated by operating-system user, VM, dev container, or physical machine rather than by path convention
- the same repository regularly needs different commit identities depending on which branch or task is being touched
- legal, compliance, or export-control rules require harder separation than a path-based convention can provide

In those cases, you should consider a different model entirely, such as:

- separate GitHub accounts or managed users
- separate SSH keys plus separate Unix users
- separate dev containers or VMs per client or per org
- per-repository local config with no shared defaults
- stronger CI enforcement around author and committer metadata

The important thing is not loyalty to this model. The important thing is choosing a model that matches the actual trust and ownership boundaries.

## Recommended Operating Policy

For a consultant or employee working across multiple orgs, the following policy is reasonable:

- keep one SSH key per org
- keep one Git email per org
- keep org repos under predictable org root paths
- keep alias naming stable and lowercase
- enable `user.useConfigOnly = true`
- verify `git config user.email` before the first commit in every newly cloned repo
- prefer cloning with the org alias from day one
- periodically inspect `git config --list --show-origin` in representative repos
- treat history rewrites as incident response, not normal workflow

Optional hardening worth considering later:

- enable GitHub's setting to block command-line pushes that expose your private email, if you rely on GitHub's private email model; GitHub says it can block pushes when the most recent commit would expose a private email on your account. Source: [Blocking command-line pushes that expose your personal email address](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/blocking-command-line-pushes-that-expose-your-personal-email-address).
- add a local helper like `git-whoami` that prints the effective SSH alias, remote URL, `user.email`, and config origin
- add a pre-push check that refuses to push if the repo path and email domain do not match policy

## Appendix: Minimal Copyable Skeleton Files

These are not complete production files, but they are useful starting points for a new machine.

### Minimal `~/.ssh/config`

```sshconfig
Host github-fuchi
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_Fuchi_jdoe_cyberdeck_27MAR2026
    IdentitiesOnly yes

Host github-cross
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_Cross_jdoe_cyberdeck_27MAR2026
    IdentitiesOnly yes

Host github-boojiboy
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_BoojiBoy_jdoe_cyberdeck_27MAR2026
    IdentitiesOnly yes

Host github-yoyodyne
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_Yoyodyne_jdoe_cyberdeck_27MAR2026
    IdentitiesOnly yes
```

### Minimal `~/.gitconfig`

```ini
[user]
    name = Jane Doe
    email = jdoe@fuchi.example
    useConfigOnly = true

[includeIf "gitdir:/home/jdoe/codebase/Fuchi/"]
    path = ~/.gitconfig-fuchi

[includeIf "gitdir:/home/jdoe/codebase/Cross/"]
    path = ~/.gitconfig-cross

[includeIf "gitdir:/home/jdoe/codebase/BoojiBoy/"]
    path = ~/.gitconfig-boojiboy

[includeIf "gitdir:/home/jdoe/codebase/Yoyodyne/"]
    path = ~/.gitconfig-yoyodyne
```

### Minimal per-org include file

```ini
[user]
    name = Jane Doe
    email = jdoe@cross.example
```

### Minimal directory skeleton

```text
~/codebase/
  Fuchi/
    actual/
  Cross/
    actual/
  BoojiBoy/
    actual/
  Yoyodyne/
    actual/
```

## Bottom Line

The central insight is that multi-org GitHub hygiene is not really an SSH problem and not really a Git problem. It is a coordination problem across SSH auth, local Git metadata, GitHub attribution, and filesystem layout.

The setup on this machine is a good default because it makes those layers explicit:

- SSH alias chooses the key
- repo path chooses the commit email
- GitHub maps that email back to the intended account
- `useConfigOnly` prevents silent fallbacks

That is the model to replicate on other machines. The exact filenames and home paths can change. The architecture should not.

## Sources

- Git configuration reference: [https://git-scm.com/docs/git-config.html](https://git-scm.com/docs/git-config.html)
- GitHub authentication overview: [https://docs.github.com/en/authentication](https://docs.github.com/en/authentication)
- GitHub multiple accounts and SSH config example: [https://docs.github.com/en/account-and-profile/how-tos/account-management/managing-multiple-accounts](https://docs.github.com/en/account-and-profile/how-tos/account-management/managing-multiple-accounts)
- GitHub SSH key setup: [https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
- GitHub SSH testing: [https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection)
- GitHub email and commit attribution: [https://docs.github.com/en/account-and-profile/concepts/email-addresses](https://docs.github.com/en/account-and-profile/concepts/email-addresses)
- GitHub commit email setup: [https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address)
- GitHub history rewriting and cleanup caveats: [https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
