---
name: vue-optimize
description: Analyzes Vue 3 component structure in client/src and produces a prioritized report of performance and code-reuse optimizations (reactivity correctness, render cost, duplicated logic, extractable composables/components). Use when asked to analyze, audit, or optimize Vue components for performance or reuse/refactoring. NOT for whole-codebase dead-code cleanup — use /optimize for that.
---

# Vue Component Optimization Analysis

This skill audits the Vue 3 frontend (`client/src/`) and produces a **prioritized, actionable report** of performance and code-reuse improvements, then optionally applies the agreed fixes. It is tuned to this app's Composition API + computed-property patterns and to the duplication that already exists in this repo.

**Scope vs. `/optimize`:** the `/optimize` command does a broad FE+BE dead-code/unused-dependency sweep. This skill is narrower and deeper: it reasons about *Vue component structure* — reactivity, render cost, and what should be lifted into shared composables/utils/components. Reach for `/optimize` to delete cruft; reach for this to restructure components.

## Workflow

1. **Pick the scope.** Default to all of `client/src/views/*.vue` and `client/src/components/*.vue`. If the user named specific files, analyze only those (plus anything they import).
2. **Run the detection toolkit** (below) to gather signal fast, then read the flagged files to confirm each finding in context. Never report a grep hit without reading the surrounding code — a `monthNames` match could be legitimately local.
3. **Classify each finding** under Performance or Reuse, assign Impact (High/Med/Low) and Effort (S/M/L), and locate it as `file:line`.
4. **Write the report** in the format below. Lead with High-impact / Low-effort items.
5. **Confirm before changing code.** Present the report and ask which items to apply. Analysis-only is a valid end state — do not refactor unprompted.
6. **If applying fixes:** per the project's root `CLAUDE.md`, **ANY create/modify of a `.vue` file MUST be delegated to the `vue-expert` subagent.** Hand it this skill's report entry as the spec. New `.js` files under `composables/` and `utils/` you may write directly. Then verify (below).

## Detection Toolkit

Run from `client/`. These surface candidates; reading confirms them.

```bash
# Component size — biggest files are the prime extraction targets
wc -l src/views/*.vue src/components/*.vue | sort -rn | head

# Reactivity API usage per file (heavy computed/watch counts hint at extractable logic)
grep -rcE "computed\(|watch\(|ref\(" src/views src/components | grep -v ":0"

# Duplicated month-name arrays (known: Dashboard, Spending, Reports — no shared util)
grep -rn "'Jan', 'Feb', 'Mar'" src

# Scattered date formatting (known: 6+ files hand-roll toLocaleDateString — no shared util)
grep -rnE "toLocaleDateString|\.getMonth\(\)" src/views src/components

# Repeated fetch/loading/error boilerplate (every view re-implements this)
grep -rlE "loading\.value|error\.value" src/views

# v-for keyed by index (project bug-magnet — CLAUDE.md rule #1)
grep -rnE ":key=\"index\"|:key=\"i\"" src

# Inline object/array/function literals in templates (new identity every render)
grep -rnE ":style=\"\{|:[a-z-]+=\"\[|@[a-z]+=\"\(\) =>|@[a-z]+=\".*=>" src
```

## Performance Dimension — what to look for

Vue 3 specifics for this codebase (Composition API, custom SVG charts, CSS-grid layouts):

- **Heavy work in the template or in non-cached getters.** Filtering/mapping/reducing the order or inventory arrays should live in a `computed` (cached), never inline in `{{ }}` or in a method called from the template (re-runs every render). The big views (`Dashboard.vue` ~1271 lines, `Spending.vue` ~852) are where this hides.
- **`v-for` + `:key="index"`.** Breaks reconciliation and is an explicit project rule — use a stable id (`sku`, `month`, `order.id`).
- **Missing `v-once` / `v-memo`** on large static or rarely-changing subtrees (e.g. rendered SVG chart axes).
- **Inline literals as props/handlers** (`:style="{...}"`, `@click="() => ..."`) — allocate a new reference each render and defeat child memoization. Hoist to a `computed` or a named handler.
- **`watch` that should be `computed`.** A `watch` that only derives state into another `ref` is a cache-miss waiting to happen — convert to `computed`.
- **Over-broad reactivity.** Large reactive objects where a `shallowRef` or plain constant would do (e.g. static config, the month-name list).
- **Redundant API calls.** Each view calling `api` in its own `onMounted` with duplicated loading/error handling; watch for refetching unchanged data on every filter tick.

## Reuse Dimension — what to look for

The repo already has the right seams — extend them, don't reinvent:
- Composables: `client/src/composables/` (`useFilters.js`, `useI18n.js`, `useAuth.js`)
- Utils: `client/src/utils/` (`currency.js` → `formatCurrency`)

Known, confirmed duplication in this repo (high-value reuse wins):

| Finding | Where | Suggested home |
|---|---|---|
| `['Jan','Feb',...,'Dec']` month array copy-pasted | `Dashboard.vue`, `Spending.vue`, `Reports.vue` | new `utils/dates.js` (`MONTH_NAMES`, `getMonthName`) |
| Hand-rolled `toLocaleDateString(...)` date formatting | 6+ views/components (`Orders`, `Spending`, `Dashboard`, `ProductDetailModal`, `BacklogDetailModal`, `ProfileDetailsModal`, `TasksModal`) | `utils/dates.js` (`formatDate`) — must honor the active locale like the existing call sites do |
| `loading` / `error` ref + `onMounted` fetch + try/catch repeated per view | all 6 views | new `composables/useApiResource.js` returning `{ data, loading, error, reload }` |
| Repeated SVG chart markup / detail-modal scaffolding | `Dashboard.vue`, `Spending.vue`, `Reports.vue`; the `*DetailModal.vue` family | extract a shared chart component / a base modal component |

General reuse heuristics: identical `<template>` blocks across components, prop-drilling that a composable would flatten, and any view over ~400 lines that mixes 3+ unrelated concerns (extract sub-components).

When proposing a new util/composable: match existing style (named exports, JSDoc-free terse comments as in `currency.js`), keep locale handling consistent with `useI18n`, and update **every** call site so the duplication is actually removed, not merely added-alongside.

## Report Format

```
# Vue Optimization Report

## Performance
1. [High impact / S effort] Dashboard.vue:455 — month aggregation runs in a method
   called from template, re-executing every render.
   Fix: move to a `computed`. ~X lines.
...

## Reuse
1. [High / S] monthNames duplicated in Dashboard.vue:455, Spending.vue:313, Reports.vue:249.
   Fix: extract `MONTH_NAMES` to utils/dates.js; import in all three.
...

## Suggested order of work
- Quick wins (High impact, S effort): #...
- Larger refactors (component extraction): #...
```

Always cite `file:line`. State impact in concrete terms (re-renders avoided, lines de-duplicated). Flag any change that risks behavior change (e.g. locale-sensitive date formatting) so the user can prioritize.

## Verification (when fixes are applied)

1. **Tests:** run the `test` skill (or `pytest tests/backend/` is unaffected; focus on frontend). Ensure no view regressed.
2. **Playwright (`mcp__playwright__*`):** start servers (`start` skill; frontend `http://localhost:3000`). `browser_navigate` to each touched route, `browser_snapshot` to confirm it renders identically, and `browser_console_messages` to assert **no new errors** (especially missing-import or undefined errors after extraction).
3. Spot-check that the **extracted code's call sites all changed** — grep for the old inline pattern; it should return zero hits.

## Checklist

- [ ] Scope chosen (all components, or the user's subset).
- [ ] Every reported finding was read in context, not just grep-matched.
- [ ] Findings classified Performance/Reuse with Impact + Effort + `file:line`.
- [ ] Report presented and the user chose what to apply (analysis-only is valid).
- [ ] Any `.vue` change went through `vue-expert`; new composables/utils follow existing style.
- [ ] Duplication actually removed at every call site (grep confirms zero remaining).
- [ ] No emojis introduced in UI (project rule).
- [ ] Verified: tests pass, routes render, no new console errors.

## Key Reminders

- **Analyze first, refactor only on request** — the deliverable is the report.
- **`vue-expert` owns every `.vue` edit** — never hand-edit a component.
- **Computed over method-in-template** is the single highest-leverage perf pattern here.
- **Extend existing seams** (`composables/`, `utils/currency.js`) rather than inventing parallel ones.
- **Locale-aware** — date/number formatting must respect `useI18n`, matching current behavior.
- This skill complements, does not replace, `/optimize` (dead-code sweep).
