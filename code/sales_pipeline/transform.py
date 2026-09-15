"""
transform.py — the **T** in ETL.

Transform is where messy input becomes numbers you can do arithmetic on. Every
function in here takes values in and returns a value out: no `input()`, no
`print()`, no files. That is what makes them easy to unit test and easy to reuse
from *any* report.

The one rule that matters: **never crash on bad data.** A single row with a price
of `"N/A"` must not take down a report covering hundreds of good rows. When a value
cannot be read, coerce it to zero and keep going.
"""


def clean_currency(value) -> float:
    """Convert a raw price into a float, using 0.0 when it cannot be read."""
    if value is None:
        return 0.0
    text = str(value).replace("$", "").replace(",", "").strip()
    try:
        return float(text)
    except ValueError:
        return 0.0


def clean_quantity(value) -> int:
    """Convert a raw quantity into an int, using 0 when it cannot be read."""
    if value is None:
        return 0
    text = str(value).strip()
    try:
        return int(text)
    except ValueError:
        return 0


def clean_sales_data(raw_data: list[dict]) -> list[dict]:
    """Clean every raw row and add the revenue it earned."""
    cleaned = []
    for row in raw_data:
        price = clean_currency(row["price"])
        qty = clean_quantity(row["qty"])
        cleaned_row = {
            "date": row["date"],
            "item": row["item"],
            "price": price,
            "qty": qty,
        }
        cleaned_row["total_revenue"] = price * qty
        cleaned.append(cleaned_row)
    return cleaned


def calculate_total_revenue(cleaned_data: list[dict]) -> float:
    """Add up the revenue of every cleaned row."""
    total = 0.0
    for row in cleaned_data:
        total += row["total_revenue"]
    return total


def summarize_by_item(cleaned_data: list[dict]) -> list[dict]:
    """Roll the row-level data up to one entry per item."""
    totals = {}
    for row in cleaned_data:
        item = row["item"]
        if item not in totals:
            totals[item] = {"item": item, "units_sold": 0, "revenue": 0.0}
        totals[item]["units_sold"] += row["qty"]
        totals[item]["revenue"] += row["total_revenue"]

    return sorted(totals.values(), key=lambda entry: (-entry["revenue"], entry["item"]))


def summarize_by_day(cleaned_data: list[dict]) -> list[dict]:
    """Roll the row-level data up to one entry per calendar day."""
    totals = {}
    for row in cleaned_data:
        date = row["date"]
        if date not in totals:
            totals[date] = {"date": date, "units_sold": 0, "revenue": 0.0}
        totals[date]["units_sold"] += row["qty"]
        totals[date]["revenue"] += row["total_revenue"]

    return sorted(totals.values(), key=lambda entry: entry["date"])


def find_top_entry(summary: list[dict], field: str = "revenue") -> dict:
    """Return the entry of `summary` with the largest value in `field`."""
    if not summary:
        return {}

    best = summary[0]
    for entry in summary[1:]:
        if entry[field] > best[field]:
            best = entry
    return best
