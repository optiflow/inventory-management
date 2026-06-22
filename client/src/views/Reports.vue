<template>
  <div class="reports">
    <div class="page-header">
      <h2>{{ t("reports.title") }}</h2>
      <p>{{ t("reports.description") }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t("common.loading") }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t("reports.quarterlyPerformance") }}</h3>
        </div>
        <div class="table-container">
          <table class="reports-table">
            <thead>
              <tr>
                <th>{{ t("reports.table.quarter") }}</th>
                <th>{{ t("reports.table.totalOrders") }}</th>
                <th>{{ t("reports.table.totalRevenue") }}</th>
                <th>{{ t("reports.table.avgOrderValue") }}</th>
                <th>{{ t("reports.table.fulfillmentRate") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="quarter in quarterlyData" :key="quarter.quarter">
                <td>
                  <strong>{{ quarter.quarter }}</strong>
                </td>
                <td>{{ quarter.total_orders }}</td>
                <td>{{ formatMoney(quarter.total_revenue) }}</td>
                <td>{{ formatMoney(quarter.avg_order_value, 2) }}</td>
                <td>
                  <span :class="getFulfillmentClass(quarter.fulfillment_rate)">
                    {{ quarter.fulfillment_rate }}%
                  </span>
                </td>
              </tr>
              <tr v-if="quarterlyData.length === 0">
                <td colspan="5" class="no-data">{{ t("common.noData") }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t("reports.monthlyRevenueTrend") }}</h3>
        </div>
        <div class="chart-container">
          <div v-if="monthlyData.length > 0" class="bar-chart">
            <div
              v-for="month in monthlyData"
              :key="month.month"
              class="bar-wrapper"
            >
              <div class="bar-container">
                <div
                  class="bar"
                  :style="{ height: getBarHeight(month.revenue) + 'px' }"
                  :title="formatMoney(month.revenue)"
                ></div>
              </div>
              <div class="bar-label">{{ formatMonth(month.month) }}</div>
            </div>
          </div>
          <div v-else class="no-data">{{ t("common.noData") }}</div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t("reports.monthOverMonthAnalysis") }}</h3>
        </div>
        <div class="table-container">
          <table class="reports-table">
            <thead>
              <tr>
                <th>{{ t("reports.table.month") }}</th>
                <th>{{ t("reports.table.orders") }}</th>
                <th>{{ t("reports.table.revenue") }}</th>
                <th>{{ t("reports.change") }}</th>
                <th>{{ t("reports.growthRate") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(month, index) in monthlyData" :key="month.month">
                <td>
                  <strong>{{ formatMonth(month.month) }}</strong>
                </td>
                <td>{{ month.order_count }}</td>
                <td>{{ formatMoney(month.revenue) }}</td>
                <td>
                  <span
                    v-if="index > 0"
                    :class="
                      getChangeClass(
                        month.revenue,
                        monthlyData[index - 1].revenue,
                      )
                    "
                  >
                    {{
                      getChangeValue(
                        month.revenue,
                        monthlyData[index - 1].revenue,
                      )
                    }}
                  </span>
                  <span v-else>-</span>
                </td>
                <td>
                  <span
                    v-if="index > 0"
                    :class="
                      getChangeClass(
                        month.revenue,
                        monthlyData[index - 1].revenue,
                      )
                    "
                  >
                    {{
                      getGrowthRate(
                        month.revenue,
                        monthlyData[index - 1].revenue,
                      )
                    }}
                  </span>
                  <span v-else>-</span>
                </td>
              </tr>
              <tr v-if="monthlyData.length === 0">
                <td colspan="5" class="no-data">{{ t("common.noData") }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">{{ totalRevenueLabel }}</div>
          <div class="stat-value">{{ formatMoney(totalRevenue) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">{{ t("reports.avgMonthlyRevenue") }}</div>
          <div class="stat-value">{{ formatMoney(avgMonthlyRevenue) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">{{ totalOrdersLabel }}</div>
          <div class="stat-value">{{ totalOrders }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">{{ t("reports.bestPerformingQuarter") }}</div>
          <div class="stat-value">{{ bestQuarter }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref, watch } from "vue";
import { api } from "../api";
import { useFilters } from "../composables/useFilters";
import { useI18n } from "../composables/useI18n";
import { formatCurrencyWithDecimals } from "../utils/currency";

export default {
  name: "Reports",
  setup() {
    const { t, currentLocale, currentCurrency } = useI18n();
    const loading = ref(true);
    const error = ref(null);
    const quarterlyData = ref([]);
    const monthlyData = ref([]);

    const {
      selectedPeriod,
      selectedLocation,
      selectedCategory,
      selectedStatus,
      getCurrentFilters,
    } = useFilters();

    const totalRevenue = computed(() => {
      return monthlyData.value.reduce(
        (sum, month) => sum + (month.revenue || 0),
        0,
      );
    });

    const avgMonthlyRevenue = computed(() => {
      return monthlyData.value.length > 0
        ? totalRevenue.value / monthlyData.value.length
        : 0;
    });

    const totalOrders = computed(() => {
      return monthlyData.value.reduce(
        (sum, month) => sum + (month.order_count || 0),
        0,
      );
    });

    const totalRevenueLabel = computed(() => {
      return t(
        selectedPeriod.value === "all"
          ? "reports.totalRevenueYtd"
          : "reports.totalRevenue",
      );
    });

    const totalOrdersLabel = computed(() => {
      return t(
        selectedPeriod.value === "all"
          ? "reports.totalOrdersYtd"
          : "reports.totalOrders",
      );
    });

    const bestQuarter = computed(() => {
      if (quarterlyData.value.length === 0) {
        return t("common.noData");
      }

      return quarterlyData.value.reduce((best, quarter) => {
        return quarter.total_revenue > best.total_revenue ? quarter : best;
      }, quarterlyData.value[0]).quarter;
    });

    const loadData = async () => {
      try {
        loading.value = true;
        error.value = null;
        const filters = getCurrentFilters();
        const [quarterly, monthly] = await Promise.all([
          api.getQuarterlyReports(filters),
          api.getMonthlyReportTrends(filters),
        ]);

        quarterlyData.value = quarterly;
        monthlyData.value = monthly;
      } catch (err) {
        error.value = t("reports.loadError", { message: err.message });
      } finally {
        loading.value = false;
      }
    };

    const formatMoney = (amount, decimals = 0) => {
      return formatCurrencyWithDecimals(
        amount || 0,
        currentCurrency.value,
        decimals,
      );
    };

    const formatMonth = (monthString) => {
      const [year, month] = monthString.split("-").map(Number);
      if (!year || !month) {
        return monthString;
      }

      const locale = currentLocale.value === "ja" ? "ja-JP" : "en-US";
      return new Intl.DateTimeFormat(locale, {
        year: "numeric",
        month: "short",
      }).format(new Date(year, month - 1));
    };

    const getBarHeight = (revenue) => {
      const maxRevenue = Math.max(
        ...monthlyData.value.map((month) => month.revenue || 0),
        0,
      );
      return maxRevenue > 0 ? (revenue / maxRevenue) * 200 : 0;
    };

    const getFulfillmentClass = (rate) => {
      if (rate >= 90) {
        return "badge success";
      }
      if (rate >= 75) {
        return "badge warning";
      }
      return "badge danger";
    };

    const getChangeValue = (current, previous) => {
      const change = current - previous;
      if (change > 0) {
        return `+${formatMoney(change)}`;
      }
      if (change < 0) {
        return `-${formatMoney(Math.abs(change))}`;
      }
      return formatMoney(0);
    };

    const getChangeClass = (current, previous) => {
      const change = current - previous;
      if (change > 0) {
        return "positive-change";
      }
      if (change < 0) {
        return "negative-change";
      }
      return "";
    };

    const getGrowthRate = (current, previous) => {
      if (previous === 0) {
        return t("reports.notAvailable");
      }

      const rate = ((current - previous) / previous) * 100;
      const sign = rate > 0 ? "+" : "";
      return `${sign}${rate.toFixed(1)}%`;
    };

    watch(
      [selectedPeriod, selectedLocation, selectedCategory, selectedStatus],
      () => {
        loadData();
      },
    );

    onMounted(loadData);

    return {
      t,
      loading,
      error,
      quarterlyData,
      monthlyData,
      totalRevenue,
      avgMonthlyRevenue,
      totalOrders,
      totalRevenueLabel,
      totalOrdersLabel,
      bestQuarter,
      formatMoney,
      formatMonth,
      getBarHeight,
      getFulfillmentClass,
      getChangeValue,
      getChangeClass,
      getGrowthRate,
    };
  },
};
</script>

<style scoped>
.reports {
  padding: 0;
}

.reports-table {
  width: 100%;
}

.chart-container {
  padding: 2rem 1rem;
  min-height: 300px;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 250px;
  gap: 0.5rem;
}

.bar-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  max-width: 80px;
}

.bar-container {
  height: 200px;
  display: flex;
  align-items: flex-end;
  width: 100%;
}

.bar {
  width: 100%;
  background: linear-gradient(to top, #3b82f6, #60a5fa);
  border-radius: 4px 4px 0 0;
  transition: all 0.3s;
  cursor: pointer;
}

.bar:hover {
  background: linear-gradient(to top, #2563eb, #3b82f6);
}

.bar-label {
  margin-top: 1.5rem;
  font-size: 0.75rem;
  color: #64748b;
  text-align: center;
  transform: rotate(-45deg);
  white-space: nowrap;
}

.positive-change {
  color: #16a34a;
  font-weight: 600;
}

.negative-change {
  color: #dc2626;
  font-weight: 600;
}

.no-data {
  padding: 2rem;
  text-align: center;
  color: #94a3b8;
  font-size: 0.875rem;
}
</style>
