"""
Tests for report API endpoints.
"""
from urllib.parse import urlencode


class TestReportsEndpoints:
    """Test suite for report endpoints."""

    def test_get_quarterly_reports(self, client):
        """Test getting quarterly reports."""
        response = client.get("/api/reports/quarterly")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        if data:
            report = data[0]
            assert "quarter" in report
            assert "total_orders" in report
            assert "total_revenue" in report
            assert "avg_order_value" in report
            assert "fulfillment_rate" in report

    def test_get_monthly_trends(self, client):
        """Test getting monthly report trends."""
        response = client.get("/api/reports/monthly-trends")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        if data:
            report = data[0]
            assert "month" in report
            assert "order_count" in report
            assert "revenue" in report
            assert "delivered_count" in report

    def test_monthly_trends_with_month_filter(self, client):
        """Test that monthly trends respect the month filter."""
        response = client.get("/api/reports/monthly-trends?month=2025-01")
        assert response.status_code == 200

        data = response.json()
        assert data
        assert all(report["month"] == "2025-01" for report in data)

    def test_monthly_trends_with_status_filter(self, client):
        """Test that monthly trends respect the status filter."""
        reports_response = client.get("/api/reports/monthly-trends?status=Delivered")
        orders_response = client.get("/api/orders?status=Delivered")

        assert reports_response.status_code == 200
        assert orders_response.status_code == 200

        reports = reports_response.json()
        orders = orders_response.json()

        assert sum(report["order_count"] for report in reports) == len(orders)
        assert all(report["order_count"] == report["delivered_count"] for report in reports)

    def test_quarterly_reports_with_shared_filters(self, client):
        """Test that quarterly reports match the filtered orders endpoint."""
        first_order = client.get("/api/orders").json()[0]
        query = urlencode({
            "warehouse": first_order["warehouse"],
            "category": first_order["category"],
            "status": first_order["status"],
            "month": first_order["order_date"][:7],
        })

        reports_response = client.get(f"/api/reports/quarterly?{query}")
        orders_response = client.get(f"/api/orders?{query}")

        assert reports_response.status_code == 200
        assert orders_response.status_code == 200

        reports = reports_response.json()
        orders = orders_response.json()

        assert sum(report["total_orders"] for report in reports) == len(orders)
        assert sum(report["total_revenue"] for report in reports) == sum(
            order["total_value"] for order in orders
        )

    def test_reports_with_all_filters_match_unfiltered_reports(self, client):
        """Test that 'all' report filter values match no filters."""
        query = "warehouse=all&category=all&status=all&month=all"

        assert client.get(f"/api/reports/quarterly?{query}").json() == client.get(
            "/api/reports/quarterly"
        ).json()
        assert client.get(f"/api/reports/monthly-trends?{query}").json() == client.get(
            "/api/reports/monthly-trends"
        ).json()
