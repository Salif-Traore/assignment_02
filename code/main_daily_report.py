"""
main_daily_report.py — the Operations department's report.

Finance asked *what did we sell?* and Marketing asked *which products sell?*
Operations asks a third question: *when do we sell?* Same eleven rows, same
pipeline, grouped down a different column — because staffing a shop floor needs
the calendar, not the catalogue.

Before running:  pip install -r requirements.txt

    python code/main_daily_report.py        # the fixed sample data
    python code/main_daily_report.py 42     # the generated data for seed 42
"""

import sys

from sales_pipeline import (
    get_raw_sales_data,
    clean_sales_data,
    calculate_total_revenue,
    summarize_by_day,
    find_top_entry,
    print_day_table,
)

# --- Reading the dataset seed ----------------------------------------------------

seed = None
if len(sys.argv) > 1 and sys.argv[1].strip() != "":
    seed = int(sys.argv[1])


# --- The report ------------------------------------------------------------------

print("=== OPERATIONS: Sales by Day ===")
print()

# 1. Extract
raw_data = get_raw_sales_data(seed)

# 2. Transform
clean_data = clean_sales_data(raw_data)
total_revenue = calculate_total_revenue(clean_data)
day_summary = summarize_by_day(clean_data)
busiest_by_revenue = find_top_entry(day_summary, "revenue")
busiest_by_units = find_top_entry(day_summary, "units_sold")

# 3. Load
print_day_table(day_summary)
print()
print(f"Total Revenue:          ${total_revenue:,.2f}")
print(f"Busiest day by revenue: {busiest_by_revenue['date']} (${busiest_by_revenue['revenue']:,.2f})")
print(f"Busiest day by units:   {busiest_by_units['date']} ({busiest_by_units['units_sold']} units)")