<template>
  <div class="app" :class="{ 'sidebar--collapsed': sidebarCollapsed }">
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
        <!-- Overview — dashboard/grid icon -->
        <router-link
          to="/"
          :class="{ active: $route.path === '/' }"
          :title="t('nav.overview')"
        >
          <span class="nav-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7" rx="1"/>
              <rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/>
              <rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
          </span>
          <span class="nav-label">{{ t('nav.overview') }}</span>
        </router-link>

        <!-- Inventory — package/box icon -->
        <router-link
          to="/inventory"
          :class="{ active: $route.path === '/inventory' }"
          :title="t('nav.inventory')"
        >
          <span class="nav-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73L13 2.27a2 2 0 0 0-2 0L4 6.27A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
              <line x1="12" y1="22.08" x2="12" y2="12"/>
            </svg>
          </span>
          <span class="nav-label">{{ t('nav.inventory') }}</span>
        </router-link>

        <!-- Orders — clipboard icon -->
        <router-link
          to="/orders"
          :class="{ active: $route.path === '/orders' }"
          :title="t('nav.orders')"
        >
          <span class="nav-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
              <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
              <line x1="9" y1="12" x2="15" y2="12"/>
              <line x1="9" y1="16" x2="13" y2="16"/>
            </svg>
          </span>
          <span class="nav-label">{{ t('nav.orders') }}</span>
        </router-link>

        <!-- Finance — credit card / dollar icon -->
        <router-link
          to="/spending"
          :class="{ active: $route.path === '/spending' }"
          :title="t('nav.finance')"
        >
          <span class="nav-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="1" y="4" width="22" height="16" rx="2" ry="2"/>
              <line x1="1" y1="10" x2="23" y2="10"/>
            </svg>
          </span>
          <span class="nav-label">{{ t('nav.finance') }}</span>
        </router-link>

        <!-- Demand Forecast — trending-up icon -->
        <router-link
          to="/demand"
          :class="{ active: $route.path === '/demand' }"
          :title="t('nav.demandForecast')"
        >
          <span class="nav-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
              <polyline points="17 6 23 6 23 12"/>
            </svg>
          </span>
          <span class="nav-label">{{ t('nav.demandForecast') }}</span>
        </router-link>

        <!-- Reports — bar-chart icon -->
        <router-link
          to="/reports"
          :class="{ active: $route.path === '/reports' }"
          :title="t('nav.reports')"
        >
          <span class="nav-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="20" x2="18" y2="10"/>
              <line x1="12" y1="20" x2="12" y2="4"/>
              <line x1="6" y1="20" x2="6" y2="14"/>
              <line x1="2" y1="20" x2="22" y2="20"/>
            </svg>
          </span>
          <span class="nav-label">{{ t('nav.reports') }}</span>
        </router-link>

        <!-- Collapse/expand toggle button — hidden on mobile (<768px) -->
        <button
          class="sidebar-collapse-btn"
          @click.stop="toggleCollapsed"
          :aria-label="sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
          :title="sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        >
          <span class="nav-icon">
            <!-- Chevron left when expanded, right when collapsed -->
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="collapse-chevron"
              :class="{ 'collapse-chevron--right': sidebarCollapsed }"
            >
              <polyline points="15 18 9 12 15 6"/>
            </svg>
          </span>
          <span class="nav-label">{{ sidebarCollapsed ? 'Expand' : 'Collapse' }}</span>
        </button>
      </nav>

      <!-- Pinned to the bottom. Both children open their menus UPWARD. -->
      <div class="sidebar-footer">
        <LanguageSwitcher :collapsed="sidebarCollapsed" />
        <ProfileMenu
          :collapsed="sidebarCollapsed"
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
      </div>
    </aside>

    <div class="app-main">
      <header class="topbar">
        <!-- Hamburger: visible on mobile only -->
        <button class="sidebar-toggle" @click="sidebarOpen = !sidebarOpen" aria-label="Toggle navigation">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
        <h2 class="topbar-title">{{ currentPageTitle }}</h2>
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
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { api } from './api'
import { useAuth } from './composables/useAuth'
import { useI18n } from './composables/useI18n'
import FilterBar from './components/FilterBar.vue'
import ProfileMenu from './components/ProfileMenu.vue'
import ProfileDetailsModal from './components/ProfileDetailsModal.vue'
import TasksModal from './components/TasksModal.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

const SIDEBAR_COLLAPSED_KEY = 'sidebarCollapsed'
// Tablet breakpoint: 768–1024px. Below this we switch to the off-canvas drawer.
const TABLET_MIN = 768
const TABLET_MAX = 1024

export default {
  name: 'App',
  components: {
    FilterBar,
    ProfileMenu,
    ProfileDetailsModal,
    TasksModal,
    LanguageSwitcher
  },
  setup() {
    const { currentUser } = useAuth()
    const { t } = useI18n()
    const route = useRoute()
    const showProfileDetails = ref(false)
    const showTasks = ref(false)
    const apiTasks = ref([])
    const sidebarOpen = ref(false)

    // ---- Collapsed state ----
    // Read persisted preference from localStorage. If not set, default to false.
    let persistedCollapsed = false
    try {
      const stored = localStorage.getItem(SIDEBAR_COLLAPSED_KEY)
      if (stored !== null) {
        persistedCollapsed = stored === 'true'
      }
    } catch (e) {
      // localStorage may be unavailable in some environments — fail silently.
    }
    const sidebarCollapsed = ref(persistedCollapsed)

    // Persist changes to localStorage whenever the user explicitly toggles.
    const persistCollapsed = (value) => {
      try {
        localStorage.setItem(SIDEBAR_COLLAPSED_KEY, String(value))
      } catch (e) {
        // Fail silently.
      }
    }

    const toggleCollapsed = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
      persistCollapsed(sidebarCollapsed.value)
    }

    // ---- Auto-collapse on tablet (768–1024px) ----
    // On tablet we always force the rail regardless of the user's stored preference.
    // We track whether the current viewport is in the tablet range so we can
    // restore the user's preference when they return to desktop (>1024px).
    const isTabletRange = () =>
      window.innerWidth >= TABLET_MIN && window.innerWidth <= TABLET_MAX

    const applyResponsiveCollapse = () => {
      if (isTabletRange()) {
        // Force collapsed on tablet — don't persist this forced state.
        sidebarCollapsed.value = true
      } else if (window.innerWidth > TABLET_MAX) {
        // Restore user's stored preference on desktop.
        try {
          const stored = localStorage.getItem(SIDEBAR_COLLAPSED_KEY)
          sidebarCollapsed.value = stored === 'true'
        } catch (e) {
          sidebarCollapsed.value = false
        }
      }
      // Below TABLET_MIN (mobile) — the drawer rules; collapsed state is irrelevant.
    }

    // Merge mock tasks from currentUser with API tasks
    const tasks = computed(() => {
      return [...currentUser.value.tasks, ...apiTasks.value]
    })

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

    const loadTasks = async () => {
      try {
        apiTasks.value = await api.getTasks()
      } catch (err) {
        console.error('Failed to load tasks:', err)
      }
    }

    const addTask = async (taskData) => {
      try {
        const newTask = await api.createTask(taskData)
        // Add new task to the beginning of the array
        apiTasks.value.unshift(newTask)
      } catch (err) {
        console.error('Failed to add task:', err)
      }
    }

    const deleteTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const isMockTask = currentUser.value.tasks.some(t => t.id === taskId)

        if (isMockTask) {
          // Remove from mock tasks
          const index = currentUser.value.tasks.findIndex(t => t.id === taskId)
          if (index !== -1) {
            currentUser.value.tasks.splice(index, 1)
          }
        } else {
          // Remove from API tasks
          await api.deleteTask(taskId)
          apiTasks.value = apiTasks.value.filter(t => t.id !== taskId)
        }
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }

    const toggleTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const mockTask = currentUser.value.tasks.find(t => t.id === taskId)

        if (mockTask) {
          // Toggle mock task status
          mockTask.status = mockTask.status === 'pending' ? 'completed' : 'pending'
        } else {
          // Toggle API task
          const updatedTask = await api.toggleTask(taskId)
          const index = apiTasks.value.findIndex(t => t.id === taskId)
          if (index !== -1) {
            apiTasks.value[index] = updatedTask
          }
        }
      } catch (err) {
        console.error('Failed to toggle task:', err)
      }
    }

    onMounted(() => {
      loadTasks()
      // Set initial collapsed state based on viewport
      applyResponsiveCollapse()
      window.addEventListener('resize', applyResponsiveCollapse)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', applyResponsiveCollapse)
    })

    return {
      t,
      showProfileDetails,
      showTasks,
      tasks,
      addTask,
      deleteTask,
      toggleTask,
      sidebarOpen,
      sidebarCollapsed,
      toggleCollapsed,
      currentPageTitle
    }
  }
}
</script>

<style>
/* ============================================================
   Design tokens — single source of truth for color, spacing,
   radii, shadows, layout dimensions, and z-index layers.
   ============================================================ */
:root {
  /* ---- Color: surfaces & text ---- */
  --color-bg:            #f8fafc;  /* app background (body)              */
  --color-surface:       #ffffff;  /* cards, sidebar, topbar             */
  --color-surface-alt:   #f8fafc;  /* table head, hover rows, inputs     */
  --color-text:          #0f172a;  /* headings / strong text             */
  --color-text-body:     #1e293b;  /* body text                          */
  --color-text-muted:    #475569;  /* table cells / secondary headings   */
  --color-text-subtle:   #64748b;  /* labels, subtitles, inactive nav    */
  --color-text-faint:    #94a3b8;  /* placeholders, icons                */

  /* ---- Color: borders ---- */
  --color-border:        #e2e8f0;  /* default borders                    */
  --color-border-strong: #cbd5e1;  /* hover borders / inputs             */
  --color-border-faint:  #f1f5f9;  /* table row separators               */

  /* ---- Color: brand / primary ---- */
  --color-primary:        #2563eb;
  --color-primary-hover:  #1d4ed8;
  --color-primary-soft:   #eff6ff;  /* active nav pill background         */
  --color-focus-border:   #3b82f6;
  --color-focus-ring:     rgba(59, 130, 246, 0.1);

  /* ---- Color: semantic (bg / text pairs, match current badges) ---- */
  --color-success:      #10b981;  --color-success-bg: #d1fae5;  --color-success-text: #065f46;
  --color-warning:      #f59e0b;  --color-warning-bg: #fed7aa;  --color-warning-text: #92400e;
  --color-danger:       #dc2626;  --color-danger-bg:  #fecaca;  --color-danger-text:  #991b1b;
  --color-info-bg:      #dbeafe;  --color-info-text:  #1e40af;

  /* ---- Spacing scale (4px base) ---- */
  --space-1: 0.25rem;   /*  4px */
  --space-2: 0.5rem;    /*  8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */

  /* ---- Radii ---- */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 10px;
  --radius-xl: 12px;

  /* ---- Shadows ---- */
  --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.10);

  /* ---- Layout dimensions ---- */
  --sidebar-width:      240px;
  --sidebar-rail-width: 72px;    /* collapsed icon rail (tablet)         */
  --topbar-height:      60px;    /* slimmer than the old 70px top nav    */
  --content-max-width:  1600px;  /* preserved from old layout            */

  /* ---- Z-index layers (single source of truth) ---- */
  --z-filterbar:      80;
  --z-topbar:         90;
  --z-sidebar:        100;
  --z-dropdown:       1000;  /* ProfileMenu / LanguageSwitcher menus      */
  --z-modal-backdrop: 1100;
  --z-modal:          1200;
}

/* ============================================================
   Base reset + body
   ============================================================ */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: var(--color-bg);
  color: var(--color-text-body);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app { min-height: 100vh; }

/* ============================================================
   Sidebar
   ============================================================ */
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
  /* Smooth width transition for manual collapse/expand */
  transition: width 0.2s ease;
  /* overflow must remain visible so footer dropdowns (LanguageSwitcher,
     ProfileMenu) can escape the 72px rail without being clipped.
     Label-overflow during the transition is prevented by white-space:nowrap
     on .nav-label and by overflow-x:hidden scoped to .sidebar-nav only. */
  overflow: visible;
}

.sidebar-logo {
  display: flex;
  flex-direction: column; /* stacked — dropped old baseline + border-left divider */
  gap: var(--space-1);
  padding: var(--space-5) var(--space-5) var(--space-4);
  border-bottom: 1px solid var(--color-border);
  /* Prevent content from wrapping/overflowing during width transition */
  overflow: hidden;
  white-space: nowrap;
  flex-shrink: 0;
}

.sidebar-logo h1 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.025em;
  transition: font-size 0.2s ease, text-align 0.2s ease;
}

.sidebar-logo .subtitle {
  font-size: 0.75rem;
  color: var(--color-text-subtle);
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  /* Hide horizontal scrollbar that appears during transition */
  overflow-x: hidden;
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
  white-space: nowrap;
}

.sidebar-nav a:hover {
  background: var(--color-surface-alt);
  color: var(--color-text);
}

.sidebar-nav a.active {
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

/* Left accent bar on active link — replaces the old horizontal bottom border */
.sidebar-nav a.active::before {
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

.nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Prevent nav labels from wrapping to a second line during the width
   transition — the parent .sidebar-nav has overflow-x:hidden so any
   momentarily-overflowing text is clipped there, not at .sidebar level. */
.nav-label {
  white-space: nowrap;
  overflow: hidden;
}

/* ---- Collapse toggle button ---- */
.sidebar-collapse-btn {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  color: var(--color-text-subtle);
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.938rem;
  width: 100%;
  text-align: left;
  transition: all 0.15s ease;
  white-space: nowrap;
  margin-top: auto;
}

.sidebar-collapse-btn:hover {
  background: var(--color-surface-alt);
  color: var(--color-text);
}

/* Chevron rotates: points left (expanded) → right (collapsed) */
.collapse-chevron {
  transition: transform 0.2s ease;
}

.collapse-chevron--right {
  transform: rotate(180deg);
}

.sidebar-footer {
  margin-top: auto; /* pins footer to the bottom of the sidebar */
  border-top: 1px solid var(--color-border);
  padding: var(--space-3);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-2);
  /* No overflow:hidden — footer dropdowns open upward and must escape. */
  flex-shrink: 0;
}

/* ============================================================
   Main column
   ============================================================ */
.app-main {
  margin-left: var(--sidebar-width);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  /* Smooth margin transition mirrors the sidebar width transition */
  transition: margin-left 0.2s ease;
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

/* Hamburger button — visible only on mobile (<768px) */
.sidebar-toggle {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text-subtle);
  padding: var(--space-2);
  border-radius: var(--radius-sm);
  align-items: center;
  justify-content: center;
  transition: color 0.15s ease;
}

.sidebar-toggle:hover {
  color: var(--color-text);
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: var(--content-max-width);
  margin: 0 auto; /* centers within the offset .app-main */
  padding: var(--space-6) var(--space-8);
}

.sidebar-backdrop {
  display: none;
}

/* ============================================================
   Collapsed / rail styles — shared by the manual toggle class
   (.sidebar--collapsed on .app) and the tablet media query.
   Factored into a single mixin block so both paths are identical.
   ============================================================ */

/* --- Rail styles applied via the .sidebar--collapsed class (manual toggle,
       desktop/tablet >768px). This class sits on .app so we use descendant
       selectors to reach sidebar, nav, footer, and app-main. --- */
.sidebar--collapsed .sidebar {
  width: var(--sidebar-rail-width);
}

.sidebar--collapsed .sidebar .nav-label,
.sidebar--collapsed .sidebar-logo .subtitle {
  display: none;
}

.sidebar--collapsed .sidebar-logo h1 {
  font-size: 1rem;
  text-align: center;
}

.sidebar--collapsed .sidebar-nav a {
  justify-content: center;
}

.sidebar--collapsed .sidebar-collapse-btn {
  justify-content: center;
}

.sidebar--collapsed .app-main {
  margin-left: var(--sidebar-rail-width);
}

/* Collapsed footer: stack vertically so items don't overflow the 72px rail */
.sidebar--collapsed .sidebar-footer {
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-1);
}

/* ============================================================
   Responsive
   ============================================================ */

/* Tablet (768–1024px): auto icon rail via media query.
   The JS resize handler also forces sidebarCollapsed=true in this range,
   so .sidebar--collapsed applies anyway — but the media query acts as a
   safety net for the width/margin even if JS hasn't run yet. */
@media (max-width: 1024px) {
  .sidebar { width: var(--sidebar-rail-width); }
  .sidebar .nav-label,
  .sidebar-logo .subtitle { display: none; }
  .sidebar-logo h1 { font-size: 1rem; text-align: center; }
  .sidebar-nav a { justify-content: center; }
  .sidebar-collapse-btn { justify-content: center; }
  .app-main { margin-left: var(--sidebar-rail-width); }
  /* Footer compact on tablet rail */
  .sidebar-footer {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--space-2);
    padding: var(--space-3) var(--space-1);
  }
}

/* Mobile: off-canvas drawer */
@media (max-width: 768px) {
  .sidebar {
    width: var(--sidebar-width);
    transform: translateX(-100%);
    transition: transform 0.2s ease, width 0.2s ease;
  }
  /* When the drawer is open on mobile, always show full labels regardless
     of sidebarCollapsed — the class-based collapsed styles are overridden. */
  .sidebar .nav-label,
  .sidebar-logo .subtitle { display: block; }
  .sidebar--collapsed .sidebar .nav-label,
  .sidebar--collapsed .sidebar-logo .subtitle { display: block; }
  .sidebar-nav a { justify-content: flex-start; }
  .sidebar--collapsed .sidebar-nav a { justify-content: flex-start; }
  .sidebar-collapse-btn { justify-content: flex-start; }
  .sidebar--collapsed .sidebar-collapse-btn { justify-content: flex-start; }
  .sidebar-logo h1 { font-size: 1.25rem; text-align: left; }
  .sidebar--collapsed .sidebar-logo h1 { font-size: 1.25rem; text-align: left; }
  /* Restore footer row layout inside the mobile drawer */
  .sidebar-footer,
  .sidebar--collapsed .sidebar-footer {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-3);
  }
  .sidebar--open {
    transform: translateX(0);
    box-shadow: var(--shadow-lg);
  }
  /* Mobile: sidebar--collapsed on .app must NOT shrink sidebar width — drawer wins */
  .sidebar--collapsed .sidebar {
    width: var(--sidebar-width);
  }
  .app-main { margin-left: 0; }
  .sidebar--collapsed .app-main { margin-left: 0; }
  .sidebar-toggle { display: inline-flex; }
  /* Hide the collapse chevron button on mobile — irrelevant for the drawer */
  .sidebar-collapse-btn { display: none; }
  .sidebar-backdrop {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.4);
    z-index: calc(var(--z-sidebar) - 1);
  }
}

/* ============================================================
   Shared global selectors (used by all 7 views).
   Token-ized but names are preserved — do NOT rename or remove.
   ============================================================ */

.page-header {
  margin-bottom: var(--space-6);
}

.page-header h2 {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 0.375rem;
  letter-spacing: -0.025em;
}

.page-header p {
  color: var(--color-text-subtle);
  font-size: 0.938rem;
}

/* ---- Stats grid + KPI cards (softly elevated, hover shadow) ---- */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-5);
  margin-bottom: var(--space-6);
}

.stat-card {
  background: var(--color-surface);
  padding: var(--space-5);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: var(--color-border-strong);
  box-shadow: var(--shadow-md);
}

.stat-label {
  color: var(--color-text-subtle);
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.625rem;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.025em;
}

.stat-card.warning .stat-value { color: #ea580c; }
.stat-card.success .stat-value { color: #059669; }
.stat-card.danger  .stat-value { color: var(--color-danger); }
.stat-card.info    .stat-value { color: var(--color-primary); }

/* ---- Card (data cards — crisp and flat, 1px border, no heavy shadow) ---- */
.card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  border: 1px solid var(--color-border);
  margin-bottom: var(--space-5);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
  padding-bottom: 0.875rem;
  border-bottom: 1px solid var(--color-border);
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.025em;
}

.table-container {
  overflow-x: auto;
}

/* ---- Tables (crisp and flat — 1px borders, no heavy shadows) ---- */
table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: var(--color-surface-alt);
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

th {
  text-align: left;
  padding: 0.5rem 0.75rem;
  font-weight: 600;
  color: var(--color-text-muted);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td {
  padding: 0.5rem 0.75rem;
  border-top: 1px solid var(--color-border-faint);
  color: #334155;
  font-size: 0.875rem;
}

tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background: var(--color-surface-alt);
}

/* ---- Badges ---- */
.badge {
  display: inline-block;
  padding: 0.313rem 0.75rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.badge.success    { background: var(--color-success-bg);  color: var(--color-success-text); }
.badge.warning    { background: var(--color-warning-bg);  color: var(--color-warning-text); }
.badge.danger     { background: var(--color-danger-bg);   color: var(--color-danger-text); }
.badge.info       { background: var(--color-info-bg);     color: var(--color-info-text); }
.badge.increasing { background: var(--color-success-bg);  color: var(--color-success-text); }
.badge.decreasing { background: var(--color-danger-bg);   color: var(--color-danger-text); }
.badge.stable     { background: #e0e7ff; color: #3730a3; }
.badge.high       { background: var(--color-danger-bg);   color: var(--color-danger-text); }
.badge.medium     { background: var(--color-warning-bg);  color: var(--color-warning-text); }
.badge.low        { background: var(--color-info-bg);     color: var(--color-info-text); }

/* ---- State helpers ---- */
.loading {
  text-align: center;
  padding: 3rem;
  color: var(--color-text-subtle);
  font-size: 0.938rem;
}

.error {
  background: #fef2f2;
  border: 1px solid var(--color-danger-bg);
  color: var(--color-danger-text);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  margin: var(--space-4) 0;
  font-size: 0.938rem;
}
</style>
