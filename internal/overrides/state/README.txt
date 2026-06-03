Internal State Files
====================

This directory holds short-lived repository-maintenance state for TheKnowledge
itself.

Files
-----
- `pending-commit-changes.txt`: queue brief commit-ready summaries here while
  maintenance work is in flight. The standardized commit helper uses the
  nonblank contents as commit body text and clears the file after a successful
  local commit.
  This queue is not durable release history. When a repository needs durable
  user-facing, operator-facing, or release-facing history, copy or summarize
  notable entries into `CHANGELOG.md` before the queue is cleared.
