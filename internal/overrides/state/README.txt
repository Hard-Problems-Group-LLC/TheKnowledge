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
