import pandas as pd

ALLOWED_COUNTRIES = [
    "France",
    "Germany",
    "Italy",
    "Morocco",
    "Tunisia",
]


def clean_orders(orders: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    required_columns = {
        "order_id",
        "date",
        "customer_id",
        "country",
        "product",
        "quantity",
        "unit_price",
    }
    missing_columns = required_columns.difference(orders.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required order columns: {', '.join(sorted(missing_columns))}"
        )

    invalid_country = ~orders["country"].isin(ALLOWED_COUNTRIES)
    rejected = orders.loc[invalid_country].copy()
    rejected["reject_reason"] = "unknown_country"
    clean = orders.loc[~invalid_country].copy()
    return clean, rejected
