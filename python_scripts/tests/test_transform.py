import pandas as pd
import pytest
from transform.transform_orders import transform_orders


# 1. A Fixture to create sample data for our tests
@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4],
            "customer_id": [101, 102, 103, 104],
            "order_date": ["2026-11-01", "2026-11-01", "2026-11-02", "2026-11-02"],
            "product": ["Laptop", "Mouse", "Keyboard", "Monitor"],
            "quantity": [1, 2, None, 5],  # Row 3 has missing quantity
            "unit_price": [85000, 1500, 3500, 25000],
            "status": ["completed", "COMPLETED ", "pending", "cancelled"],  # Messy text
        }
    )


# 2. Test that missing values are dropped
def test_remove_missing_values(sample_data):
    result = transform_orders(sample_data)

    # We started with 4 rows, but row 3 has a NULL quantity, so it should be dropped.
    # That means only 3 rows should remain.
    assert len(result) == 3


# 3. Test that text is cleaned (lowercased and trimmed)
def test_clean_status_text(sample_data):
    result = transform_orders(sample_data)

    # Row 2 had "COMPLETED " with a space and uppercase.
    # Our function should have changed it to "completed"
    row_2_status = result[result["order_id"] == 2]["status"].iloc[0]
    assert row_2_status == "completed"


# 4. Test the math (Revenue Calculation)
def test_calculate_total_amount(sample_data):
    result = transform_orders(sample_data)

    # Row 1: 1 Laptop * 85,000 = 85,000
    row_1_total = result[result["order_id"] == 1]["total_amount"].iloc[0]
    assert row_1_total == 85000

    # Row 2: 2 Mice * 1,500 = 3,000
    row_2_total = result[result["order_id"] == 2]["total_amount"].iloc[0]
    assert row_2_total == 3000
