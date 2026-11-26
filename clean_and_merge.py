"""clean_and_merge.py - Data pipeline for the MIS2001 data workflow exercise.

Steps:
1. Read the two data files (data/order.txt and data/customer.txt)
2. Clean duplicate rows
3. Convert all amounts to CNY into a new column 'amount_cny'
4. Merge order data and customer data on 'customer_id'
5. Write the merged data to an SQLite database
6. Create a summary table: average 'amount_cny' by region

Run:  python clean_and_merge.py
"""

import sqlite3

import pandas as pd

DB_PATH = "orders.db"
ORDERS_PATH = "data/order.txt"
CUSTOMERS_PATH = "data/customer.txt"

# Conversion rates to CNY
RATES = {"USD": 6.9, "EUR": 7.5, "CNY": 1.0, "JPY": 0.05}


def build_database():
    # 1. Read the two data files (comma-separated TXT)
    orders = pd.read_csv(ORDERS_PATH)
    customers = pd.read_csv(CUSTOMERS_PATH)

    # 2. Clean the duplicates
    orders = orders.drop_duplicates()
    customers = customers.drop_duplicates()

    # 3. Convert all amount values to CNY -> new column 'amount_cny'
    orders["amount_cny"] = orders.apply(
        lambda row: row["amount"] * RATES.get(row["currency"], 1.0), axis=1
    )

    # 4. Connect (merge) order data and customer data on 'customer_id'
    merged = orders.merge(customers, on="customer_id", how="inner")

    # 5. Write the merged data to an SQLite database
    conn = sqlite3.connect(DB_PATH)
    merged.to_sql("orders_merged", conn, if_exists="replace", index=False)

    # 6. Summary table: average 'amount_cny' by region
    summary = merged.groupby("region", as_index=False)["amount_cny"].mean()
    summary = summary.rename(columns={"amount_cny": "avg_amount_cny"})
    summary.to_sql("summary_by_region", conn, if_exists="replace", index=False)

    conn.close()

    print(f"Merged rows written to '{DB_PATH}' table 'orders_merged':")
    print(merged.to_string(index=False))
    print("\nSummary (avg amount_cny by region) written to table 'summary_by_region':")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    build_database()
