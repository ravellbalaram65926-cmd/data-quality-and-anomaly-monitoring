"""ETL demo: validate event records, quarantine invalid rows, and report metrics."""

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "raw" / "sample_events.csv"
DEFAULT_OUTPUT = ROOT / "data" / "gold"
REQUIRED = ("event_id", "customer_id", "event_time", "amount")


def validate_rows(input_path: Path) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    with input_path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    seen = set()
    clean = []
    rejected = []
    reasons = {"duplicate": 0, "missing_required": 0, "negative_amount": 0}
    for row in rows:
        reason = ""
        key = row.get("event_id", "")
        if key in seen:
            reason = "duplicate"
        elif any(not row.get(column, "").strip() for column in REQUIRED):
            reason = "missing_required"
        elif float(row["amount"]) < 0:
            reason = "negative_amount"
        if reason:
            reasons[reason] += 1
            rejected.append({**row, "reject_reason": reason})
        else:
            seen.add(key)
            clean.append(row)
    return clean, rejected, reasons


def run_quality(input_path: Path, output_dir: Path) -> dict[str, int]:
    clean, rejected, reasons = validate_rows(input_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, rows in (("clean_events.csv", clean), ("quarantine.csv", rejected)):
        fields = list(rows[0]) if rows else list(REQUIRED) + (["reject_reason"] if filename == "quarantine.csv" else [])
        with (output_dir / filename).open("w", newline="", encoding="utf-8") as target:
            writer = csv.DictWriter(target, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    metrics = {
        "input_rows": len(clean) + len(rejected),
        "accepted_rows": len(clean),
        "rejected_rows": len(rejected),
        **reasons,
    }
    (output_dir / "quality_report.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    metrics = run_quality(args.input, args.output_dir)
    print(json.dumps(metrics, sort_keys=True))


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
