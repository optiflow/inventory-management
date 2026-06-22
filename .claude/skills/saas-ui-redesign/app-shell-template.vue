<!--
  REFERENCE SKELETON for the redesigned client/src/App.vue.

  This is a guide, not a drop-in file. vue-expert adapts it to the live
  App.vue, preserving ALL existing setup() logic (tasks, modals, i18n).
  Only the template shell and the <style> are restructured.

  Key points illustrated below:
    - aside.sidebar  (logo + vertical nav + footer with language/profile)
    - .app-main      (offset by the sidebar, holds topbar + filterbar + content)
    - header.topbar  (slim bar showing the current page title)
    - Replace nav icons' <!-- icon --> comments with real inline SVG (NO emojis).
-->
<template>
  <div class="app">
    <!-- Mobile-only backdrop; shown when the off-canvas drawer is open -->
    <div
      v-if="sidebarOpen"
      class="sidebar-backdrop"
      @click="sidebarOpen = false"
    ></div>

    <aside class="sidebar" :class="{ 'sidebar--open': sidebarOpen }">
      <div class="sidebar-logo">
        <h1>{{ t('nav.companyName') }}</h1>
        <span class="subtitle">{{ t('nav.subtitle') }}</span>
      </div>

      <nav class="sidebar-nav" @click="sidebarOpen = false">
        <router-link to="/" :class="{ active: $route.path === '/' }">
          <span class="nav-icon"><!-- inline SVG --></span>
          <span class="nav-label">{{ t('nav.overview') }}</span>
        </router-link>
        <router-link to="/inventory" :class="{ active: $route.path === '/inventory' }">
          <span class="nav-icon"><!-- inline SVG --></span>
          <span class="nav-label">{{ t('nav.inventory') }}</span>
        </router-link>
        <router-link to="/orders" :class="{ active: $route.path === '/orders' }">
          <span class="nav-icon"><!-- inline SVG --></span>
          <span class="nav-label">{{ t('nav.orders') }}</span>
        </router-link>
        <router-link to="/spending" :class="{ active: $route.path === '/spending' }">
          <span class="nav-icon"><!-- inline SVG --></span>
          <span class="nav-label">{{ t('nav.finance') }}</span>
        </router-link>
        <router-link to="/demand" :class="{ active: $route.path === '/demand' }">
          <span class="nav-icon"><!-- inline SVG --></span>
          <span class="nav-label">{{ t('nav.demandForecast') }}</span>
        </router-link>
        <router-link to="/reports" :class="{ active: $route.path === '/reports' }">
          <span class="nav-icon"><!-- inline SVG --></span>
          <span class="nav-label">{{ t('nav.reports') }}</span>
        </router-link>
      </nav>

      <!-- Pinned to the bottom. Both children must open their menus UPWARD. -->
      <div class="sidebar-footer">
        <LanguageSwitcher />
        <ProfileMenu
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
      </div>
    </aside>

    <div class="app-main">
      <header class="topbar">
        <button class="sidebar-toggle" @click="sidebarOpen = !sidebarOpen" aria-label="Toggle navigation">
          <span class="nav-icon"><!-- hamburger inline SVG --></span>
        </button>
        <h2 class="topbar-title">{{ currentPageTitle }}</h2>
        <!-- right-side slot reserved for future actions -->
      </header>

      <FilterBar />

      <main class="main-content">
        <router-view />
      </main>
    </div>

    <ProfileDetailsModal
      :is-open="showProfileDetails"
      @close="showProfileDetails = false"
    />

    <TasksModal
      :is-open="showTasks"
      :tasks="tasks"
      @close="showTasks = false"
      @add-task="addTask"
      @delete-task="deleteTask"
      @toggle-task="toggleTask"
    />
  </div>
</template>

<script>
// Keep ALL existing imports and setup() logic from the current App.vue.
// Add only: a `sidebarOpen` ref and a `currentPageTitle` computed.
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
// ... existing imports (api, useAuth, useI18n, components) ...

export default {
  name: 'App',
  components: { /* ... unchanged ... */ },
  setup() {
    // ... existing: useAuth(), useI18n() -> { t }, showProfileDetails,
    //     showTasks, apiTasks, tasks, loadTasks, addTask, deleteTask,
    //     toggleTask, onMounted(loadTasks) ...

    const route = useRoute()
    const sidebarOpen = ref(false)

    // Map each route path to the SAME i18n key its nav link uses.
    const TITLE_KEYS = {
      '/': 'nav.overview',
      '/inventory': 'nav.inventory',
      '/orders': 'nav.orders',
      '/spending': 'nav.finance',
      '/demand': 'nav.demandForecast',
      '/reports': 'nav.reports'
    }
    const currentPageTitle = computed(() => t(TITLE_KEYS[route.path] || 'nav.overview'))

    return {
      // ... existing returns ...
      sidebarOpen,
      currentPageTitle
    }
  }
}
</script>

<style>
/*
  1. Paste the :root token block from design-tokens.css here first.
  2. Keep the existing global selectors (.page-header, .card, .stat-card,
     table, .badge, .loading, .error) — the 7 views depend on them.
     Token-ize their hardcoded values but DO NOT rename or remove them.
  3. Replace .top-nav / .nav-container / .nav-tabs rules with the layout below.
*/

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--color-bg);
  color: var(--color-text-body);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app { min-height: 100vh; }

/* ---- Sidebar ---- */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: var(--sidebar-width);
  height: 100vh;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  z-index: var(--z-sidebar);
}

.sidebar-logo {
  display: flex;
  flex-direction: column;       /* stacked — drop the old border-left divider */
  gap: var(--space-1);
  padding: var(--space-5) var(--space-5) var(--space-4);
  border-bottom: 1px solid var(--color-border);
}
.sidebar-logo h1 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.025em;
}
.sidebar-logo .subtitle {
  font-size: 0.75rem;
  color: var(--color-text-subtle);
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-2);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}
.sidebar-nav a {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  color: var(--color-text-subtle);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.938rem;
  transition: all 0.15s ease;
}
.sidebar-nav a:hover {
  background: var(--color-surface-alt);
  color: var(--color-text);
}
.sidebar-nav a.active {
  background: var(--color-primary-soft);
  color: var(--color-primary);
}
.sidebar-nav a.active::before {   /* left accent bar (replaces old bottom border) */
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 60%;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  background: var(--color-primary);
}
.nav-icon { width: 20px; height: 20px; flex-shrink: 0; display: inline-flex; }

.sidebar-footer {
  margin-top: auto;             /* pins footer to the bottom */
  border-top: 1px solid var(--color-border);
  padding: var(--space-3);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-2);
  /* No overflow:hidden here — footer dropdowns must escape upward. */
}

/* ---- Main column ---- */
.app-main {
  margin-left: var(--sidebar-width);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.topbar {
  position: sticky;
  top: 0;
  height: var(--topbar-height);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 0 var(--space-8);
  z-index: var(--z-topbar);
}
.topbar-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.025em;
}
.sidebar-toggle {
  display: none;                /* visible only on mobile */
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text-subtle);
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: var(--content-max-width);
  margin: 0 auto;               /* centers within the offset .app-main */
  padding: var(--space-6) var(--space-8);
}

.sidebar-backdrop {
  display: none;
}

/* ---- Responsive ---- */
@media (max-width: 1024px) {
  .sidebar { width: var(--sidebar-rail-width); }
  .sidebar .nav-label,
  .sidebar-logo .subtitle { display: none; }    /* icon rail */
  .sidebar-logo h1 { font-size: 1rem; text-align: center; }
  .sidebar-nav a { justify-content: center; }
  .app-main { margin-left: var(--sidebar-rail-width); }
}

@media (max-width: 768px) {
  .sidebar {
    width: var(--sidebar-width);
    transform: translateX(-100%);
    transition: transform 0.2s ease;
  }
  .sidebar .nav-label,
  .sidebar-logo .subtitle { display: block; }
  .sidebar-nav a { justify-content: flex-start; }
  .sidebar--open { transform: translateX(0); box-shadow: var(--shadow-lg); }
  .app-main { margin-left: 0; }
  .sidebar-toggle { display: inline-flex; }
  .sidebar-backdrop {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.4);
    z-index: calc(var(--z-sidebar) - 1);
  }
}
</style>
