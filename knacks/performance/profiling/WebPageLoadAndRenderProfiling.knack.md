# Web Page Load And Render Profiling

Load this knack when a web page "finishes loading" long before it is ready for
a human to use. Build a repeatable audit utility that measures when
a route becomes structurally complete, stable, and ready for use.

For modern client applications, the browser's built-in milestones are useful
but incomplete. `DOMContentLoaded` means the document was parsed. `load`
means document-tied subresources finished loading. Neither one tells you
whether later script work populated the page, whether layout stopped shifting,
or whether background updates are still mutating the critical elements the
user is waiting on.

Treat this as a layered readiness problem. A serious audit utility should
distinguish at least four moments:

1. navigation milestone reached;
2. page shell and expected elements exist in the DOM;
3. the route's first meaningful render is complete; and
4. the page enters a short quiet window with no meaningful structural churn.

## Mental Model

"Fully loaded" and "fully rendered" are product definitions, not browser
standards. That is why generic waits so often disappoint. A page can reach the
`load` event and still spend seconds fetching data, inflating long lists,
resizing cards, swapping placeholders, or restyling after fonts, widgets, or
hydration settle in.

The right audit utility therefore combines three signal families:

- browser-native timing data for coarse milestones;
- project-owned readiness indicators for semantic meaning; and
- observer-based settling checks for visual and structural stability.

The browser-native layer tells you when navigation and resource loading
occurred. The project-owned layer tells you when the application believes the
route is ready. The observer layer checks whether the page is still bouncing
around after that claim.

## Recommended Tooling Shape

Playwright is a strong default for this work because it can drive realistic
navigation, inject instrumentation before page scripts run, wait on DOM-side
predicates, and capture traces when a scenario is suspicious. Use it to build
a project-local utility under the consuming application's own `scripts/` tree.
Do not rely on one-off ad hoc snippets when you intend to compare routes over
time.

A useful audit utility should usually do the following:

1. launch the target page with explicit viewport, authentication state, cache
   policy, and network or CPU profile;
2. install instrumentation before app code runs;
3. navigate to a representative route and trigger any representative user
   actions;
4. wait for project-specific readiness plus a short stability window;
5. emit structured results such as JSON; and
6. optionally save a Playwright trace for slow or failed runs.

## Instrument Before The App Runs

Install instrumentation with Playwright's init-script support before route
code executes. That lets the utility observe timing, DOM mutation, resizing,
performance entries from the beginning of the navigation rather than halfway
through the interesting part.

Inside that instrumentation, maintain a lightweight page-local audit object
that records:

- navigation timing data;
- counts and timestamps for subtree mutations in the critical app container;
- size changes for important layout containers;
- layout-shift and long-task entries when the browser exposes them;
- project-owned readiness attributes or performance marks; and
- the timestamp of the last meaningful structural change.

Do not monitor the entire DOM if the application has stable containers you can
target. Watching everything creates noise and inflated observer overhead.

## Add Project-Owned Readiness Signals

This is the highest-value recommendation in the knack. If the application owns
the rendering pipeline, it should expose its own readiness contract.

A practical pattern is a stable route container with attributes such as:

- `data-load-state="loading|loaded"`
- `data-update-state="idle|updating"`
- `data-route-key="..."`
- `data-render-revision="..."`

Use `loading` for structural work: adding the route shell, mounting the main
component tree, resolving enough asynchronous data that the page will stop
reflowing dramatically, and inserting the elements a user must see before the
page is meaningfully present. Switch to `loaded` only after that structure is
in place.

Use `updating` for later value refreshes that should not count as initial
route load. That keeps the audit focused on first-route readiness instead of
perpetual background activity.

If the project already uses the Performance API, custom `performance.mark()`
events such as `route:shell-ready`, `route:content-ready`, or
`route:first-usable` are also useful.

## Define A Real Settling Rule

Avoid pretending that one browser event means "fully rendered." In Playwright,
`networkidle` is explicitly discouraged as a general readiness check, and it
is especially weak for modern applications with polling, analytics,
websockets, or lazy hydration. Use it, if at all, only as one weak hint among
several.

A better rule is: declare the route complete only after semantic readiness is
true and a short quiet window has passed.

A quiet window usually means all of these are true for some bounded interval,
often a few hundred milliseconds:

- the route container reports `data-load-state="loaded"`;
- the route container does not report `data-update-state="updating"`;
- no meaningful subtree mutations occurred in the critical container;
- no meaningful container resizes occurred;
- no new layout-shift entries appeared; and
- no long main-thread task crossed the threshold you care about.

After that quiet window, wait for one or two animation frames before taking
the final timestamp. That gives the browser a chance to present the settled
state instead of measuring just before the next repaint.

## What To Measure

The audit report should separate milestones instead of collapsing everything
into one number. A good baseline output often includes:

- time to `DOMContentLoaded`;
- time to `load`;
- time to first project-owned shell-ready marker;
- time to first project-owned content-ready or usable marker;
- time to semantic `loaded`;
- time to update-idle after the initial route load; and
- time to quiet-window completion.

Also collect supporting evidence:

- mutation count and last mutation timestamp;
- resize count for critical containers;
- cumulative layout-shift data when available;
- long-task count and worst observed duration when available; and
- route metadata such as viewport, scenario name, cache mode, and auth state.

## Suggested Audit Flow

1. Pick a representative scenario matrix: cold cache, warm cache, desktop,
   mobile, anonymous, authenticated, and any data-heavy route variants that
   matter operationally.
2. Install page instrumentation before navigation.
3. Navigate with `commit`, `domcontentloaded`, or `load` as coarse milestones,
   but do not stop there.
4. Wait on a project-specific predicate with Playwright's DOM-evaluation
   support. This predicate should read the readiness attributes or custom
   marks, not guess from arbitrary text.
5. Continue waiting until the quiet-window rule passes.
6. Emit structured output and attach a trace when thresholds are exceeded.

Keep the utility deterministic. Stable fixtures, known viewports, and
explicit scenario setup are more valuable than broad fuzziness when the goal
is trend comparison.

## Anti-Patterns

- Treating `load` as synonymous with fully rendered.
- Treating `networkidle` as authoritative for single-page applications.
- Using fixed sleeps such as "wait five seconds and hope."
- Measuring only one happy-path route under a warm local cache.
- Inferring readiness from spinner disappearance alone when the page can still
  be reflowing.
- Watching the full document for every mutation when one app-root container
  would do.
- Returning only a single timing number with no supporting evidence.
- Capturing no trace, DOM state, or observer summary for slow outliers.

## Further Information

- Playwright, `Page` API reference:
  <https://playwright.dev/docs/api/class-page>
- Playwright, evaluating JavaScript in the page:
  <https://playwright.dev/docs/evaluating>
- Playwright, tracing:
  <https://playwright.dev/docs/api/class-tracing>
- MDN, `PerformanceNavigationTiming`:
  <https://developer.mozilla.org/en-US/docs/Web/API/PerformanceNavigationTiming>
- MDN, `PerformanceObserver`:
  <https://developer.mozilla.org/en-US/docs/Web/API/PerformanceObserver>
- MDN, `MutationObserver`:
  <https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver>
- MDN, Resize Observer API:
  <https://developer.mozilla.org/en-US/docs/Web/API/Resize_Observer_API>
- MDN, `requestAnimationFrame()`:
  <https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame>
- MDN, `PerformanceLongTaskTiming`:
  <https://developer.mozilla.org/en-US/docs/Web/API/PerformanceLongTaskTiming>
- web.dev, "Debug layout shifts":
  <https://web.dev/articles/debug-layout-shifts>
