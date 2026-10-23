from pathlib import Path

import pandas as pd
import pytest

from run_pipeline import run
from pipeline.transform import clean_orders


def make_orders(rows: list[dict[str, object]]) -> pd.DataFrame:
    return pd.DataFrame(
        rows,
        columns=[
            "order_id",
            "date",
            "customer_id",
            "country",
            "product",
            "quantity",
            "unit_price",
        ],
    )


def test_unknown_country_is_rejected() -> None:
    orders = make_orders(
        [
            {
                "order_id": 1,
                "date": "2026-10-05",
                "customer_id": "C001",
                "country": "Spain",
                "product": "Keyboard",
                "quantity": 1,
                "unit_price": 45.0,
            },
            {
                "order_id": 2,
                "date": "2026-10-05",
                "customer_id": "C002",
                "country": "Italy",
                "product": "Headset",
                "quantity": 1,
                "unit_price": 59.5,
            },
        ]
    )

    clean, rejected = clean_orders(orders)

    assert list(clean["order_id"]) == [2]
    assert list(rejected["order_id"]) == [1]
    assert list(rejected["reject_reason"]) == ["unknown_country"]


def test_missing_required_column_is_reported() -> None:
    orders = pd.DataFrame({"country": ["France"]})

    with pytest.raises(ValueError, match="Missing required order columns"):
        clean_orders(orders)


def test_run_writes_revenue_and_rejected_order_reports(tmp_path: Path) -> None:
    orders = make_orders(
        [
            {
                "order_id": 1,
                "date": "2026-10-05",
                "customer_id": "C001",
                "country": "France",
                "product": "Monitor",
                "quantity": 2,
                "unit_price": 229.0,
            },
            {
                "order_id": 2,
                "date": "2026-10-05",
                "customer_id": "C002",
                "country": "Spain",
                "product": "Keyboard",
                "quantity": 1,
                "unit_price": 45.0,
            },
        ]
    )
    input_path = tmp_path / "orders.csv"
    output_dir = tmp_path / "output"
    orders.to_csv(input_path, index=False)

    assert run(input_path, output_dir) == 458.0
    assert pd.read_csv(output_dir / "revenue_by_country.csv").to_dict("records") == [
        {"country": "France", "revenue": 458.0}
    ]
    assert pd.read_csv(output_dir / "rejected_orders.csv")["reject_reason"].tolist() == [
        "unknown_country"
    ]


def test_every_allowed_country_is_kept() -> None:
    countries = ["France", "Germany", "Italy", "Morocco", "Tunisia"]
    orders = make_orders(
        [
            {
                "order_id": index,
                "date": "2026-10-05",
                "customer_id": f"C{index:03}",
                "country": country,
                "product": "Monitor",
                "quantity": 1,
                "unit_price": 10.0,
            }
            for index, country in enumerate(countries, start=1)
        ]
    )

    clean, rejected = clean_orders(orders)

    assert clean["country"].tolist() == countries
    assert rejected.empty


def test_initial_day_one_data_matches_guide_total(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "data" / "raw" / "orders_day1.csv"

    assert len(pd.read_csv(input_path)) == 30
    assert run(input_path, tmp_path / "output") == 7655.90


def test_initial_day_one_data_rejects_five_unknown_countries() -> None:
    project_root = Path(__file__).resolve().parents[1]
    orders = pd.read_csv(project_root / "data" / "raw" / "orders_day1.csv")

    clean, rejected = clean_orders(orders)

    assert len(clean) == 25
    assert len(rejected) == 5
    assert rejected["reject_reason"].eq("unknown_country").all()
