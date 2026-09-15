"""
sales_pipeline — a small ETL package for the sales data.
"""

# --- The public API -------------------------------------------------------------

from .extract import get_raw_sales_data

from .transform import (
    clean_sales_data,
    calculate_total_revenue,
    summarize_by_item,
    summarize_by_day,
    find_top_entry,
)

from .display import (
    print_sales_table,
    print_item_table,
    print_day_table,
)

__all__ = [
    "get_raw_sales_data",
    "clean_sales_data",
    "calculate_total_revenue",
    "summarize_by_item",
    "summarize_by_day",
    "find_top_entry",
    "print_sales_table",
    "print_item_table",
    "print_day_table",
]
