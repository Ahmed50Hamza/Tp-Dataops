import argparse
from pathlib import Path

import pandas as pd

from pipeline.transform import clean_orders


def run(input_path: Path, output_dir: Path) -> float:
    orders = pd.read_csv(input_path)
    clean, rejected = clean_orders(orders)
    clean["revenue"] = (
        pd.to_numeric(clean["quantity"], errors="raise")
        * pd.to_numeric(clean["unit_price"], errors="raise")
    )
    total = float(clean["revenue"].sum())

    output_dir.mkdir(parents=True, exist_ok=True)
    clean.groupby("country", as_index=False)["revenue"].sum().to_csv(
        output_dir / "revenue_by_country.csv", index=False
    )
    rejected.to_csv(output_dir / "rejected_orders.csv", index=False)
    print(f"TOTAL: {total:.2f}")
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean orders and report revenue.")
    parser.add_argument("input_csv", type=Path)
    parser.add_argument(
        "--output-dir", type=Path, default=Path("data/output")
    )
    args = parser.parse_args()
    run(args.input_csv, args.output_dir)


if __name__ == "__main__":
    main()
