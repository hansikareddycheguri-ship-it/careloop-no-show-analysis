"""
Task 1.1 — Read the file the foundations way (csv module only, no pandas)

Reads data/appointments.csv with csv.DictReader, converts the numeric columns,
and splits rows into `accepted` and `rejected`. Rejected rows are saved to
rejected_rows.json.
"""

import csv
import json

INPUT_PATH = "data/appointments.csv"
REJECTED_PATH = "rejected_rows.json"


def parse_row(row):
    """Return a copy of `row` with numeric columns converted.

    age, fee_inr, prior_no_shows -> int
    distance_km                  -> float

    Raises ValueError if any of these values cannot be converted
    (for example an empty string).
    """
    parsed = dict(row)
    parsed["age"] = int(row["age"])
    parsed["fee_inr"] = int(row["fee_inr"])
    parsed["prior_no_shows"] = int(row["prior_no_shows"])
    parsed["distance_km"] = float(row["distance_km"])
    return parsed


accepted = []
rejected = []

with open(INPUT_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames
    rows = list(reader)

print("Header:", header)
print("Row count:", len(rows))

for line_no, row in enumerate(rows, start=2):  # line 1 is the header
    try:
        accepted.append(parse_row(row))
    except ValueError as e:
        rejected.append({"line": line_no, "error": str(e), "row": row})

print("Accepted rows:", len(accepted))
print("Rejected rows:", len(rejected))

with open(REJECTED_PATH, "w", encoding="utf-8") as f:
    json.dump(rejected, f, indent=2)

print(f"Saved {len(rejected)} rejected rows to {REJECTED_PATH}")
