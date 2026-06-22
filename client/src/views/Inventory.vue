<template>
  <div class="inventory">
    <div class="page-header">
      <h2>{{ t("inventory.title") }}</h2>
      <p>{{ t("inventory.description") }}</p>
    </div>

    <div
      v-if="!loading && !error && showLowStockAlert"
      class="low-stock-alert"
      role="status"
      aria-live="polite"
    >
      <div class="low-stock-alert-main">
        <div class="low-stock-alert-copy">
          <div class="low-stock-alert-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M8.257 3.099c.765-1.36 2.72-1.36 3.486 0l6.516 11.588c.75 1.334-.213 2.98-1.743 2.98H3.484c-1.53 0-2.493-1.646-1.743-2.98L8.257 3.1zM11 14a1 1 0 10-2 0 1 1 0 002 0zm-1-2a1 1 0 01-1-1V7a1 1 0 112 0v4a1 1 0 01-1 1z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <div>
            <h3>
              {{
                t("inventory.lowStockAlertTitle", {
                  count: lowStockItems.length,
                })
              }}
            </h3>
            <p>{{ t("inventory.lowStockAlertDescription") }}</p>
          </div>
        </div>
        <button
          type="button"
          class="low-stock-dismiss"
          :aria-label="t('inventory.dismissLowStockAlert')"
          :title="t('inventory.dismissLowStockAlert')"
          @click="lowStockAlertDismissed = true"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>

      <ul class="low-stock-list">
        <li v-for="item in lowStockPreview" :key="item.id">
          <button type="button" @click="showItemDetail(item)">
            <span>
              <strong>{{ item.sku }}</strong>
              {{ translateProductName(item.name) }}
            </span>
            <span v-if="getLowStockShortfall(item) > 0">
              {{
                t("inventory.lowStockShortfall", {
                  count: getLowStockShortfall(item),
                })
              }}
            </span>
            <span v-else>{{ t("inventory.atReorderPoint") }}</span>
          </button>
        </li>
      </ul>

      <p v-if="remainingLowStockCount > 0" class="low-stock-more">
        {{
          t("inventory.lowStockMore", {
            count: remainingLowStockCount,
          })
        }}
      </p>
    </div>

    <div v-if="loading" class="loading">{{ t("common.loading") }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">
            {{ t("inventory.stockLevels") }} ({{ filteredItems.length }}
            {{ t("inventory.skus") }})
          </h3>
          <div class="inventory-actions">
            <button
              type="button"
              class="export-csv-button"
              :disabled="filteredItems.length === 0"
              :title="t('inventory.exportCsv')"
              @click="exportInventoryCsv"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M3 3a1 1 0 011-1h8.586A2 2 0 0114 2.586L17.414 6A2 2 0 0118 7.414V17a1 1 0 01-1 1H4a1 1 0 01-1-1V3zm10 1.414V7h2.586L13 4.414zM5 4v12h11V9h-4a1 1 0 01-1-1V4H5zm3 7a1 1 0 011-1h3a1 1 0 110 2H9a1 1 0 01-1-1zm0 3a1 1 0 011-1h5a1 1 0 110 2H9a1 1 0 01-1-1z"
                  clip-rule="evenodd"
                />
              </svg>
              <span>{{ t("inventory.exportCsv") }}</span>
            </button>
            <div class="search-box">
              <svg
                class="search-icon"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                  clip-rule="evenodd"
                />
              </svg>
              <input
                v-model="searchQuery"
                type="text"
                :placeholder="t('inventory.searchPlaceholder')"
                class="search-input"
              />
              <button
                v-if="searchQuery"
                @click="searchQuery = ''"
                class="clear-search"
                :title="t('inventory.clearSearch')"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
        <div v-if="filteredItems.length === 0" class="inventory-empty">
          <strong>
            {{
              items.length === 0
                ? t("inventory.emptyInventory")
                : t("inventory.emptySearchResults")
            }}
          </strong>
          <p v-if="searchQuery.trim()">{{ t("inventory.emptySearchHint") }}</p>
        </div>
        <div v-else class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t("inventory.table.sku") }}</th>
                <th>{{ t("inventory.table.itemName") }}</th>
                <th>{{ t("inventory.table.category") }}</th>
                <th>{{ t("inventory.table.quantityOnHand") }}</th>
                <th>{{ t("inventory.table.reorderPoint") }}</th>
                <th>{{ t("inventory.table.unitCost") }}</th>
                <th>{{ t("inventory.table.totalValue") }}</th>
                <th>{{ t("inventory.table.location") }}</th>
                <th>{{ t("inventory.table.status") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in filteredItems"
                :key="item.id"
                class="clickable-row"
                @click="showItemDetail(item)"
              >
                <td>
                  <strong>{{ item.sku }}</strong>
                </td>
                <td>{{ translateProductName(item.name) }}</td>
                <td>{{ translateCategory(item.category) }}</td>
                <td>
                  <strong>{{ item.quantity_on_hand }}</strong>
                </td>
                <td>{{ item.reorder_point }}</td>
                <td>{{ currencySymbol }}{{ item.unit_cost.toFixed(2) }}</td>
                <td>
                  <strong
                    >{{ currencySymbol
                    }}{{
                      (item.quantity_on_hand * item.unit_cost).toLocaleString(
                        undefined,
                        { minimumFractionDigits: 2, maximumFractionDigits: 2 },
                      )
                    }}</strong
                  >
                </td>
                <td>{{ translateWarehouse(item.location) }}</td>
                <td>
                  <span :class="['badge', getStockStatusClass(item)]">
                    {{ getStockStatus(item) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <InventoryDetailModal
      :is-open="showItemModal"
      :inventory-item="selectedItem"
      @close="showItemModal = false"
    />
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from "vue";
import { api } from "../api";
import { useFilters } from "../composables/useFilters";
import { useI18n } from "../composables/useI18n";
import InventoryDetailModal from "../components/InventoryDetailModal.vue";

export default {
  name: "Inventory",
  components: {
    InventoryDetailModal,
  },
  setup() {
    const { t, currentCurrency, translateProductName, translateWarehouse } =
      useI18n();

    const currencySymbol = computed(() => {
      return currentCurrency.value === "JPY" ? "¥" : "$";
    });

    const loading = ref(true);
    const error = ref(null);
    const items = ref([]);
    const searchQuery = ref("");
    const lowStockAlertDismissed = ref(false);

    // Modal state
    const showItemModal = ref(false);
    const selectedItem = ref(null);

    // Use shared filters
    const { selectedLocation, selectedCategory, getCurrentFilters } =
      useFilters();

    // Stock status order for sorting (using status keys)
    const STATUS_ORDER = { lowStock: 0, adequate: 1, inStock: 2 };

    // Get stock status key (for sorting and translation)
    const getStockStatusKey = (item) => {
      if (item.quantity_on_hand <= item.reorder_point) {
        return "lowStock";
      } else if (item.quantity_on_hand <= item.reorder_point * 1.5) {
        return "adequate";
      } else {
        return "inStock";
      }
    };

    const getLowStockShortfall = (item) =>
      Math.max(item.reorder_point - item.quantity_on_hand, 0);

    const translateCategory = (category) => {
      const categoryMap = {
        "Circuit Boards": t("categories.circuitBoards"),
        Sensors: t("categories.sensors"),
        Actuators: t("categories.actuators"),
        Controllers: t("categories.controllers"),
        "Power Supplies": t("categories.powerSupplies"),
      };
      return categoryMap[category] || category;
    };

    const lowStockItems = computed(() => {
      return items.value
        .filter((item) => item.quantity_on_hand <= item.reorder_point)
        .slice()
        .sort((a, b) => {
          const shortfallDelta =
            getLowStockShortfall(b) - getLowStockShortfall(a);

          if (shortfallDelta !== 0) return shortfallDelta;

          return a.sku.localeCompare(b.sku);
        });
    });

    const lowStockPreview = computed(() => lowStockItems.value.slice(0, 5));

    const remainingLowStockCount = computed(() =>
      Math.max(lowStockItems.value.length - lowStockPreview.value.length, 0),
    );

    const showLowStockAlert = computed(
      () => lowStockItems.value.length > 0 && !lowStockAlertDismissed.value,
    );

    const normalizeSearchValue = (value) =>
      value === null || value === undefined
        ? ""
        : String(value).toLowerCase();

    const itemMatchesSearch = (item, query) => {
      const searchableFields = [
        item.sku,
        item.name,
        translateProductName(item.name),
        item.category,
        translateCategory(item.category),
        item.warehouse,
        translateWarehouse(item.warehouse),
        item.location,
        translateWarehouse(item.location),
        getStockStatusKey(item),
        getStockStatus(item),
      ];

      return searchableFields.some((field) =>
        normalizeSearchValue(field).includes(query),
      );
    };

    // Computed property to filter items by search query and sort by stock status
    const filteredItems = computed(() => {
      let filtered = items.value;

      // Apply search filter if query exists
      if (searchQuery.value.trim()) {
        const query = searchQuery.value.toLowerCase().trim();
        filtered = filtered.filter((item) => itemMatchesSearch(item, query));
      }

      // Sort by stock status: Low Stock first, then Adequate, then In Stock
      // Always create a copy to avoid mutating the original array
      return filtered.slice().sort((a, b) => {
        const statusA = getStockStatusKey(a);
        const statusB = getStockStatusKey(b);
        return STATUS_ORDER[statusA] - STATUS_ORDER[statusB];
      });
    });

    const loadInventory = async () => {
      try {
        loading.value = true;
        const filters = getCurrentFilters();
        // Inventory doesn't support month/status filters, only warehouse and category
        items.value = await api.getInventory({
          warehouse: filters.warehouse,
          category: filters.category,
        });
        lowStockAlertDismissed.value = false;
      } catch (err) {
        error.value = "Failed to load inventory: " + err.message;
      } finally {
        loading.value = false;
      }
    };

    // Watch for filter changes and reload data
    watch([selectedLocation, selectedCategory], () => {
      loadInventory();
    });

    const getStockStatus = (item) => {
      const key = getStockStatusKey(item);
      return t(`status.${key}`);
    };

    const getStockStatusClass = (item) => {
      if (item.quantity_on_hand <= item.reorder_point) {
        return "danger";
      } else if (item.quantity_on_hand <= item.reorder_point * 1.5) {
        return "warning";
      } else {
        return "success";
      }
    };

    const formatCsvValue = (value) => {
      const text = value === null || value === undefined ? "" : String(value);
      return /[",\n\r]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
    };

    const exportInventoryCsv = () => {
      if (filteredItems.value.length === 0) return;

      const headers = [
        t("inventory.table.sku"),
        t("inventory.table.itemName"),
        t("inventory.table.category"),
        t("inventory.table.quantityOnHand"),
        t("inventory.table.reorderPoint"),
        t("inventory.table.unitCost"),
        t("inventory.table.totalValue"),
        t("inventory.table.location"),
        t("inventory.table.status"),
      ];

      const rows = filteredItems.value.map((item) => [
        item.sku,
        translateProductName(item.name),
        translateCategory(item.category),
        item.quantity_on_hand,
        item.reorder_point,
        item.unit_cost.toFixed(2),
        (item.quantity_on_hand * item.unit_cost).toFixed(2),
        translateWarehouse(item.location),
        getStockStatus(item),
      ]);

      const csv = [headers, ...rows]
        .map((row) => row.map(formatCsvValue).join(","))
        .join("\n");
      const blob = new Blob([`\uFEFF${csv}`], {
        type: "text/csv;charset=utf-8;",
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = "inventory.csv";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    };

    const showItemDetail = (item) => {
      selectedItem.value = item;
      showItemModal.value = true;
    };

    onMounted(loadInventory);

    return {
      t,
      loading,
      error,
      items,
      searchQuery,
      lowStockAlertDismissed,
      filteredItems,
      lowStockItems,
      lowStockPreview,
      remainingLowStockCount,
      showLowStockAlert,
      getStockStatus,
      getStockStatusClass,
      getLowStockShortfall,
      translateCategory,
      exportInventoryCsv,
      showItemModal,
      selectedItem,
      showItemDetail,
      currencySymbol,
      translateProductName,
      translateWarehouse,
    };
  },
};
</script>

<style scoped>
.page-header {
  margin-bottom: 1.5rem;
}

.page-header h2 {
  margin-bottom: 0.25rem;
}

.page-header p {
  color: var(--color-text-subtle);
  font-size: 0.875rem;
}

.low-stock-alert {
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid var(--color-danger-bg);
  border-radius: var(--radius-md);
  background: var(--color-danger-soft);
  color: var(--color-danger-text);
}

.low-stock-alert-main {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.low-stock-alert-copy {
  display: flex;
  gap: 0.75rem;
}

.low-stock-alert-icon {
  display: flex;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 999px;
  background: var(--color-danger-bg);
}

.low-stock-alert-icon svg,
.low-stock-dismiss svg {
  width: 1rem;
  height: 1rem;
}

.low-stock-alert h3 {
  margin: 0 0 0.25rem;
  color: var(--color-danger-text);
  font-size: 0.938rem;
  font-weight: 700;
}

.low-stock-alert p {
  margin: 0;
  font-size: 0.875rem;
}

.low-stock-dismiss {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  padding: 0.25rem;
  border: 0;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-danger-text);
  cursor: pointer;
}

.low-stock-dismiss:hover {
  background: var(--color-danger-bg);
}

.low-stock-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.5rem;
  margin: 0.875rem 0 0;
  padding: 0;
  list-style: none;
}

.low-stock-list button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid var(--color-danger-bg);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: var(--color-text-body);
  font: inherit;
  text-align: left;
  cursor: pointer;
}

.low-stock-list button:hover {
  border-color: var(--color-danger);
}

.low-stock-list button span:last-child {
  flex: 0 0 auto;
  color: var(--color-danger-text);
  font-size: 0.75rem;
  font-weight: 700;
}

.low-stock-more {
  margin-top: 0.75rem;
  color: var(--color-danger-text);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--color-border);
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text);
  margin: 0;
}

.inventory-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-left: auto;
}

.export-csv-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  flex: 0 0 auto;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.export-csv-button:hover:not(:disabled) {
  border-color: var(--color-text-faint);
  background: var(--color-surface-alt);
}

.export-csv-button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.export-csv-button svg {
  width: 16px;
  height: 16px;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  min-width: 300px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  width: 18px;
  height: 18px;
  color: var(--color-text-faint);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.5rem 2.5rem 0.5rem 2.5rem;
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  color: var(--color-text);
  background: var(--color-surface-alt);
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-focus-border);
  background: var(--color-surface);
  box-shadow: 0 0 0 3px var(--color-focus-ring);
}

.search-input::placeholder {
  color: var(--color-text-faint);
}

.clear-search {
  position: absolute;
  right: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  color: var(--color-text-faint);
  cursor: pointer;
  transition: all 0.2s;
}

.clear-search:hover {
  background: var(--color-border);
  color: var(--color-text-subtle);
}

.clear-search svg {
  width: 18px;
  height: 18px;
}

.inventory-empty {
  padding: 2.5rem 1rem;
  text-align: center;
  color: var(--color-text-subtle);
}

.inventory-empty strong {
  display: block;
  margin-bottom: 0.375rem;
  color: var(--color-text);
  font-size: 0.938rem;
}

.inventory-empty p {
  margin: 0;
  font-size: 0.875rem;
}

.loading,
.error {
  padding: 2rem;
  text-align: center;
  color: var(--color-text-subtle);
}

.error {
  color: var(--color-danger);
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.clickable-row:hover {
  background: var(--color-primary-soft) !important;
}

@media (max-width: 768px) {
  .card-header {
    align-items: stretch;
    flex-direction: column;
    gap: 1rem;
  }

  .inventory-actions {
    align-items: stretch;
    flex-direction: column;
    margin-left: 0;
  }

  .export-csv-button {
    justify-content: center;
  }

  .search-box {
    min-width: 0;
    width: 100%;
  }
}
</style>
