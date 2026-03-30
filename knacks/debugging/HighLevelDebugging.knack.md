# High-Level Debugging

Load this knack when a failure is real but the route from symptom to cause is
not. This guide stays above any particular language, tool, architecture, or
platform. Its purpose is to help a human and an AI assistant debug in a way
that produces evidence, isolates causes, and avoids the failure modes that
AI often makes worse.

## Mental Model

High-level debugging is not "trying fixes until the symptom goes away." It is
structured search under uncertainty. The real goal is to explain the gap
between expected behavior and observed behavior well enough to do three
things:

1. restore correct behavior;
2. identify the smallest set of causal factors worth calling the bug; and
3. reduce the chance that the same failure family returns unnoticed.

That mindset matters for AI-assisted work. A model can generate plausible
stories much faster than it can discover truth. If the session is not
anchored in evidence, an AI assistant often accelerates the wrong loop:
bigger guesses, faster.

Treat every bug as a claim that reality differs from the current model. The
debugging job is to improve the model by collecting observations, forming
hypotheses, and running tests that can rule causes in or out. This is close
to the hypothetico-deductive method described in Google's SRE
troubleshooting guidance, and it is still the best default frame for AI work.

## Core Loop

### State The Problem Precisely

Start with a crisp problem report:

- what was expected;
- what actually happened;
- how the failure can be reproduced, if known; and
- what changed around the time it appeared.

If the report is vague, the AI will fill gaps with pattern-matching. That is
useful for brainstorming, but dangerous for diagnosis. Force the issue into a
precise claim before asking for a fix.

### Reproduce And Stabilize

A bug that cannot be reproduced may still be real, but it is much harder to
reason about. The first strong move is usually to make the failure happen
again in a controlled way, then define the exact condition that counts as
"the same failure." Precise failure conditions matter because they prevent
false diagnoses and "fixes" that merely change the visible symptom.

### Reduce The Failure Surface

Good debuggers shrink the problem. Reduce the failing case, inputs, sequence,
or state until you have the smallest case that still fails for the same
reason. A minimized case does three useful things at once: it removes noise,
sharpens hypotheses, and makes it harder for the AI to anchor on irrelevant
details.

Reduction is one of the highest-leverage AI debugging techniques because it
changes the prompt quality, not just the model output. Smaller, better-scoped
failure cases usually beat bigger prompts full of mixed evidence.

### Generate Multiple Plausible Hypotheses

Do not ask the AI for "the cause" too early. Ask for several plausible causes
ranked by likelihood, plus the evidence each one predicts. The goal is to
force discriminating theories that can be tested.

This counters two common failures: human confirmation bias and model
confabulation. A single polished explanation feels satisfying. A list of
competing explanations is much easier to falsify.

### Run Discriminating Tests

The best next action is usually the smallest test that separates hypotheses.
Change one thing at a time when practical. Preserve notes on what
you changed and what you observed. Negative results are not wasted effort.
They narrow the search space and often become the most reusable artifact from
the session.

AI is especially helpful here when used as an experiment designer: "What is
the cheapest observation that would make hypothesis A much less likely than
hypothesis B?"

### Separate Diagnosis From Repair

Do not let the session jump from symptom to final patch without an explicit
diagnosis checkpoint. Once the likely cause is identified, ask what minimal
change addresses that cause, what nearby behavior could regress, and how to
tell whether the change fixes the root problem instead of merely hiding it.

### Validate The Fix Broadly

A repair is not finished when the symptom disappears once. Check that the
original failure is gone, that the minimized case now behaves correctly, that
closely related scenarios still work, and that the system has not moved into
a different bad state. Good debugging closes the loop with explanation, not
just silence.

## Techniques That Tend To Work Well With AI

- Give the model primary artifacts rather than narrative summaries whenever
  possible. Observations, exact failures, narrowed reproductions, and dated
  notes are better than "something seems wrong around here."
- Ask the model to explain the observed behavior before asking it to rewrite
  anything. Recent self-debugging research suggests that explanation and
  "rubber duck" style reasoning can improve correction quality.
- Ask for predicted observations, not just causes. A useful hypothesis says
  what else should be true if it is correct.
- Use the model to propose smaller experiments, boundary cases, and
  reductions. AI is often better at generating candidate probes than at
  picking the winning theory without feedback.
- Keep a running case log. Long debugging sessions degrade when either the
  human or the model forgets which ideas were tried already.
- Preserve failed attempts and disconfirming evidence. Research and
  operations guidance both support the idea that negative results are part of
  the solution, not embarrassment to erase.
- Ask for adjacent-risk review after a likely fix. "What else could break for
  the same reason?" is often more valuable than "optimize this patch."

## Anti-Patterns That Tend To Fail

- Shotgun debugging. Making several speculative changes at once destroys the
  ability to learn from the result and gives the AI no clean feedback loop.
- Context by storytelling. When the AI sees a condensed story instead of raw
  observations, it may optimize for narrative coherence rather than truth.
- Treating correlation as causation. A nearby change, noisy metric, or
  suggestive timing relationship is only a clue.
- Letting the model self-correct without external feedback. Recent research
  shows that intrinsic self-correction can stagnate or even degrade when a
  model has no new evidence.
- Repeated full rewrites after every failed attempt. Large resets usually
  erase the signal contained in partial understanding.
- Escalating instrumentation or intervention without considering side
  effects. More visibility is not always neutral; observation can perturb the
  system you are trying to understand.
- Stopping after symptom suppression. Retries, guards, or broader catch-alls
  may reduce visible pain while leaving the causal path intact.
- Ignoring uncertainty. If the diagnosis is still probabilistic, say so and
  design the next test accordingly.

## Practical Questions To Ask During AI-Assisted Debugging

- What are the exact observations, and which ones are assumptions?
- What is the smallest reproducer that still fails the same way?
- Which two hypotheses are most worth separating next?
- What result would falsify the current leading theory?
- If the proposed fix works, what else should now be true?
- If it does not work, what does that tell us rather than merely block us?

These questions keep the conversation evidence-led and make it easier to hand
the case from one person or model to another without losing the reasoning
trail.

## Further Information

- Google SRE, "Effective Troubleshooting":
  <https://sre.google/sre-book/effective-troubleshooting/>
- The Debugging Book, "Reducing Failure-Inducing Inputs":
  <https://www.debuggingbook.org/html/DeltaDebugger.html>
- NIST CSRC glossary, "Root Cause Analysis":
  <https://csrc.nist.gov/glossary/term/root_cause_analysis>
- OpenReview, "Teaching Large Language Models to Self-Debug":
  <https://openreview.net/forum?id=KuPixIqPiq>
- OpenReview, "Large Language Models Cannot Self-Correct Reasoning Yet":
  <https://openreview.net/forum?id=IkmD3fKBPQ>
- OpenReview, "Revisit Self-Debugging with Self-Generated Tests for Code
  Generation": <https://openreview.net/forum?id=hYd6BCZTzg>
- Google SRE, "Example Postmortem":
  <https://sre.google/sre-book/example-postmortem/>
