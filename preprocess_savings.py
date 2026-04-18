import csv
import json
from collections import defaultdict

INPUT_FILE = "optiship_logs.csv"
OUTPUT_FILE = "savings.json"

def preprocess():
    totals = defaultdict(lambda: {"actual_sum": 0.0, "optimal_sum": 0.0})

    with open(INPUT_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = row["user_id"].strip()
            totals[uid]["actual_sum"] += float(row["actual_cost"])
            totals[uid]["optimal_sum"] += float(row["optimal_cost"])

    result = [
        {
            "user_id": uid,
            "actual_sum": round(v["actual_sum"], 4),
            "optimal_sum": round(v["optimal_sum"], 4)
        }
        for uid, v in sorted(totals.items())
    ]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Written {len(result)} records to {OUTPUT_FILE}")

if __name__ == "__main__":
    preprocess()
