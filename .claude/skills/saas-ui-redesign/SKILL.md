---
name: saas-ui-redesign
description: Redesigns the inventory-management Vue app into a modern SaaS interface with a left vertical sidebar (replacing the top nav), a slim top bar, and a CSS design-token system. Use when asked to modernize, restyle, or redesign the app's overall layout or navigation shell — not for editing a single view's content.
---

# SaaS UI Redesign Guide

This skill converts the Factory Inventory Management app from a horizontal **top-nav** layout to a modern SaaS shell: a fixed **left sidebar** for navigation, a **slim top bar** showing the current page, the existing `FilterBar` retained as a horizontal strip inside the content area, and a shared **CSS design-token system** for consistent spacing and color.

It is tailored to this repo. The reference files in this skill directory contain the exact code to use:
- `design-tokens.css` — the `:root` token block to paste into `App.vue`.
- `app-shell-template.vue` — the redesigned `App.vue` template + layout `<style>` skeleton.

## Before / After

```
BEFORE                                  AFTER
┌────────────────────────────────┐      ┌──────┬─────────────────────────┐
│ Logo   [nav tabs]   lang  prof  │      │ Logo │ [topbar: page title]    │
├────────────────────────────────┤      │      ├─────────────────────────┤
│ FilterBar                       │      │ nav  │ FilterBar               │
├────────────────────────────────┤      │ ...  ├─────────────────────────┤
│                                 │      │      │                         │
│ router-view (max 1600px)        │      │ ───  │ router-view (max 1600px)│
│                                 │      │ lang │                         │
│                                 │      │ prof │                         │
└────────────────────────────────┘      └──────┴─────────────────────────┘
```

## MANDATORY: Delegate to vue-expert

Per the project's root `CLAUDE.md`: **ANY time you create or significantly modify a `.vue` file, you MUST delegate to the `vue-expert` subagent.** This redesign edits `.vue` and frontend files exclusively:
- `client/src/App.vue`
- `client/src/components/FilterBar.vue`
- `client/src/components/ProfileMenu.vue`, `client/src/components/LanguageSwitcher.vue` (dropdown direction fix)
- `client/src/locales/en.js`, `client/src/locales/ja.js` (add `nav.reports`)

✅ Do route the entire implementation through `vue-expert`, handing it this skill (and the two reference files) as the spec.
❌ Do NOT hand-edit these files yourself.

## Target Layout

```
.app
├── aside.sidebar          fixed; left:0; top:0; height:100vh; width 240px; z-index var(--z-sidebar)
│   ├── .sidebar-logo      company name + subtitle, STACKED vertically (drop old border-left divider)
│   ├── nav.sidebar-nav    6 vertical router-links (inline-SVG icon + label)
│   └── .sidebar-footer    margin-top:auto; LanguageSwitcher + ProfileMenu
└── .app-main              margin-left: var(--sidebar-width); flex column; min-height 100vh
    ├── header.topbar      sticky top:0; height var(--topbar-height); z-index var(--z-topbar); shows page title
    ├── FilterBar          sticky top: var(--topbar-height); z-index var(--z-filterbar)
    └── main.main-content  max-width var(--content-max-width); margin:0 auto; padding var(--space-6) var(--space-8)
        └── router-view
    ProfileDetailsModal / TasksModal   (unchanged)
```

**Active route indicator:** a filled pill (`background: var(--color-primary-soft); color: var(--color-primary)`) **plus** a 4px left accent bar via `::before`. This replaces the old `::after` 2px bottom border, which does not make sense on a vertical nav.

## Design Tokens

Paste the full `:root` block from `design-tokens.css` into the **global (non-scoped)** `<style>` of `App.vue`, above the `body` rule. Then refactor `App.vue`'s global styles and the new shell to consume the tokens.

**Scope rule (keep the diff bounded):**
- ✅ Define all tokens; token-ize `App.vue`'s global block and the new layout CSS.
- ✅ Keep every existing global selector (`.page-header`, `.card`, `.stat-card`, `table`, `.badge`, `.loading`, `.error`) — the 7 views depend on them. Token-ize their values but do NOT rename or remove them.
- ❌ Do NOT refactor per-view scoped CSS unless a color visibly clashes.

**Old → token mapping:**

| Old hardcoded value | Token |
|---|---|
| `#f8fafc` (bg) | `--color-bg` / `--color-surface-alt` |
| `#ffffff` | `--color-surface` |
| `#0f172a` | `--color-text` |
| `#1e293b` | `--color-text-body` |
| `#475569` | `--color-text-muted` |
| `#64748b` | `--color-text-subtle` |
| `#94a3b8` | `--color-text-faint` |
| `#e2e8f0` | `--color-border` |
| `#cbd5e1` | `--color-border-strong` |
| `#f1f5f9` | `--color-border-faint` |
| `#2563eb` | `--color-primary` |
| `#eff6ff` | `--color-primary-soft` |
| `0 1px 3px rgba(0,0,0,.05)` | `--shadow-sm` |
| `0 4px 12px rgba(0,0,0,.06)` | `--shadow-md` |
| `70px` (old nav height) | `--topbar-height` (now 60px) |
| `1600px` | `--content-max-width` |
| badge bg/text pairs | `--color-{success,warning,danger,info}-{bg,text}` |

## Step-by-Step Workflow

1. **Delegate to `vue-expert`** with this skill + both reference files as the spec.
2. **Add tokens:** paste `design-tokens.css`'s `:root` block into `App.vue`'s global `<style>`.
3. **Restructure the `App.vue` template** from `header.top-nav` to `aside.sidebar` + `.app-main` + `header.topbar`, per `app-shell-template.vue`. Move `LanguageSwitcher` and `ProfileMenu` into `.sidebar-footer`. Keep both modals exactly where they are. Preserve all existing `setup()` logic.
4. **Add the `nav.reports` i18n key** to `client/src/locales/en.js` (e.g. `"Reports"`) and `client/src/locales/ja.js` (translated). `App.vue` currently hardcodes the string `Reports` on its last nav link — switch it to `{{ t('nav.reports') }}`. Preserve the `/spending` → `nav.finance` label mapping.
5. **Add a `currentPageTitle` computed** to `App.vue`'s `setup()` mapping `$route.path` to the same i18n key each nav link uses; render it in the top bar.
6. **Rewrite `App.vue` global styles** to use tokens; replace `.top-nav` / `.nav-container` / `.nav-tabs` rules with `.sidebar` / `.sidebar-nav` / `.topbar` rules from the template. Keep `.main-content { max-width: var(--content-max-width); margin: 0 auto }` — centering now happens within the offset `.app-main`.
7. **Reposition `FilterBar.vue`:** change its sticky `top: 70px` → `top: var(--topbar-height)` and `z-index: 90` → `z-index: var(--z-filterbar)`. Leave its inner `max-width: 1600px` (it self-centers inside the offset column).
8. **Fix footer dropdown direction** (see Risks): make `ProfileMenu` and `LanguageSwitcher` menus open **upward**.
9. **Verify all 7 views render** (Dashboard, Inventory, Orders, Spending, Demand, Reports, Backlog) — they rely on global selectors and don't hardcode nav, so they should work; confirm none assumed the old 70px top offset.
10. **Run Playwright verification** (below) and report concisely.

## FilterBar Repositioning

`FilterBar.vue` is sticky at `top: 70px; z-index: 90` to clear the old top nav. After the redesign it sits inside `.app-main`, directly under the slim top bar:

```css
.filter-bar {            /* or whatever the root class is */
  top: var(--topbar-height);   /* was 70px */
  z-index: var(--z-filterbar);  /* was 90  */
}
```

Keep the inner container's `max-width: 1600px; margin: 0 auto`.

## Responsive Behavior

| Width | Sidebar | `.app-main` margin |
|---|---|---|
| `> 1024px` | Full 240px, labels visible | `var(--sidebar-width)` |
| `768–1024px` | Icon rail 72px, labels hidden | `var(--sidebar-rail-width)` |
| `< 768px` | Off-canvas (`translateX(-100%)`); hamburger in top bar toggles `.sidebar--open`; backdrop click closes | `0` |

The off-canvas drawer is the only net-new interactive logic: a `sidebarOpen` ref, a hamburger `<button>` in the top bar, and a `.sidebar-backdrop`. Clicking a nav link or the backdrop closes it. (MVP fallback: ship the icon rail at all small widths first, add off-canvas as an enhancement.) The exact CSS is in `app-shell-template.vue`.

## Z-Index Layering Reference

Tokens are the single source of truth. Final order (low → high):

| Layer | Token | Value |
|---|---|---|
| FilterBar | `--z-filterbar` | 80 |
| Top bar | `--z-topbar` | 90 |
| Sidebar | `--z-sidebar` | 100 |
| Footer dropdowns (Profile/Language) | `--z-dropdown` | 1000 |
| Modal backdrop | `--z-modal-backdrop` | 1100 |
| Modal | `--z-modal` | 1200 |

Modals must sit above the footer dropdowns so an open modal covers them.

## Playwright Verification

Start the servers first (`npm run dev` in `client/`, backend via the `start` skill); app at `http://localhost:3000`. Use `mcp__playwright__*` tools.

1. `browser_navigate` to each route (`/`, `/inventory`, `/orders`, `/spending`, `/demand`, `/reports`) and `browser_snapshot` each — confirm it renders and the sidebar active state matches the route.
2. `browser_resize` to **1440×900** → `browser_take_screenshot` of `/` and `/inventory`: full sidebar, content centered, FilterBar flush under the top bar.
3. `browser_resize` to **820×1024** → screenshot: icon rail, reduced left margin.
4. `browser_resize` to **390×844** → screenshot: sidebar hidden, hamburger present; `browser_click` the hamburger → screenshot the open drawer + backdrop.
5. Open the footer **ProfileMenu** and **LanguageSwitcher** → confirm both menus open **upward** and are fully visible.
6. `browser_console_messages` → assert no new errors.

## Verification Checklist

- [ ] All edits went through `vue-expert`.
- [ ] `:root` tokens defined in `App.vue`; global selectors token-ized and intact.
- [ ] Sidebar shows logo + 6 links; active route has pill + left accent bar.
- [ ] Top bar shows the correct localized page title per route.
- [ ] `nav.reports` exists in both `en.js` and `ja.js`; no hardcoded nav strings remain.
- [ ] FilterBar sits flush under the top bar (no gap/overlap).
- [ ] Footer dropdowns open upward and fully visible.
- [ ] All 7 views render correctly at desktop, tablet, and mobile widths.
- [ ] No emojis in the UI; nav icons are inline SVG.
- [ ] No new console errors.

## Key Reminders

- **vue-expert owns every edit** — never hand-edit the `.vue`/locale files.
- **No emojis** — use inline SVG for nav icons (root + client `CLAUDE.md`).
- **Don't touch view content** — only the `App.vue` shell, `FilterBar` positioning, the two dropdown components, and locale keys change. View-scoped CSS stays as-is.
- **Preserve i18n label mappings** — `/spending` shows `nav.finance`, not "Spending".
- **Keep global selectors** — `.page-header`, `.card`, `.stat-card`, `table`, `.badge`, `.loading`, `.error` are shared by all views; token-ize their values but keep the names.
- **Tokens are the source of truth** for spacing, color, and z-index — reference them, don't reintroduce hardcoded values in the new layout.
