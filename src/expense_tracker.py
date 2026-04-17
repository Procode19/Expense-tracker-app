import random
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CATEGORIES = [
    "Food",
    "Travel",
    "Rent",
    "Entertainment",
    "Shopping",
    "Health",
    "Utilities",
    "Education",
    "Bills",
    "Savings",
    "Salary",
    "Miscellaneous",
]

PAYMENT_METHODS = ["Cash", "Credit Card", "Debit Card", "UPI", "Wallet"]
TRANSACTION_TYPES = ["Expense", "Income"]

CATEGORY_DESCRIPTIONS = {
    "Food": ["Grocery store", "Restaurant", "Coffee shop", "Lunch", "Dinner"],
    "Travel": ["Taxi", "Metro ride", "Flight booking", "Fuel", "Bus ticket"],
    "Rent": ["Home rent", "Apartment rent", "Office rent"],
    "Entertainment": ["Movie", "Concert", "Streaming service", "Game"],
    "Shopping": ["Clothes", "Electronics", "Gift", "Accessories"],
    "Health": ["Medicine", "Doctor visit", "Gym membership", "Health checkup"],
    "Utilities": ["Electricity bill", "Water bill", "Internet bill", "Mobile recharge"],
    "Education": ["Course fee", "Books", "Online learning", "Workshop"],
    "Bills": ["Electricity", "Phone", "Cable", "Insurance"],
    "Savings": ["Emergency fund", "Investment", "Fixed deposit"],
    "Salary": ["Monthly salary", "Bonus", "Freelance payout"],
    "Miscellaneous": ["Gift", "Donation", "Stationery", "Other expense"],
}

DEFAULT_BUDGETS = {
    "Food": 10000,
    "Travel": 7000,
    "Rent": 15000,
    "Entertainment": 5000,
    "Shopping": 8000,
    "Health": 4000,
    "Utilities": 4500,
    "Education": 6000,
    "Bills": 5500,
    "Miscellaneous": 3000,
}

CATEGORY_WEIGHTS = {
    "Food": 0.20,
    "Travel": 0.12,
    "Rent": 0.14,
    "Entertainment": 0.08,
    "Shopping": 0.10,
    "Health": 0.07,
    "Utilities": 0.10,
    "Education": 0.05,
    "Bills": 0.08,
    "Miscellaneous": 0.06,
}

CATEGORY_BASE_AMOUNT = {
    "Food": 400,
    "Travel": 500,
    "Rent": 12000,
    "Entertainment": 1200,
    "Shopping": 1800,
    "Health": 900,
    "Utilities": 1400,
    "Education": 2200,
    "Bills": 1300,
    "Miscellaneous": 700,
}

sns.set(style="whitegrid")


def generate_synthetic_expense_data(num_records: int = 300, start_date: str = "2024-01-01", end_date: str = "2024-06-30") -> pd.DataFrame:
    """Create a synthetic expense dataset with date, category, amount, type, and payment method."""
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    categories = list(CATEGORY_WEIGHTS.keys())
    weights = list(CATEGORY_WEIGHTS.values())

    rows = []
    for _ in range(num_records):
        date = np.random.choice(dates)
        category = np.random.choice(categories, p=weights)
        txn_type = "Income" if random.random() < 0.12 and category == "Salary" else "Expense"
        if category == "Salary":
            txn_type = "Income"

        if txn_type == "Income":
            amount = round(abs(np.random.normal(loc=25000, scale=4000)), 2)
            description = random.choice(CATEGORY_DESCRIPTIONS[category])
        else:
            mean_value = CATEGORY_BASE_AMOUNT.get(category, 800)
            amount = round(abs(np.random.normal(loc=mean_value, scale=mean_value * 0.25)), 2)
            description = random.choice(CATEGORY_DESCRIPTIONS[category])

        payment_method = random.choice(PAYMENT_METHODS)
        merchant = random.choice(["Amazon", "BigBasket", "Uber", "Zomato", "Swiggy", "Airbnb", "Local Store", "Health Clinic", "Electricity Board"])
        note = "Synthetic sample data for expense tracking analysis."

        rows.append(
            {
                "Date": pd.Timestamp(date).strftime("%Y-%m-%d"),
                "Category": category,
                "Description": description,
                "Amount": amount,
                "Payment Method": payment_method,
                "Type": txn_type,
                "Merchant": merchant,
                "Note": note,
            }
        )

    df = pd.DataFrame(rows)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


def clean_expense_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw expense data and create feature columns for analysis."""
    df = df.copy()
    df = df.drop_duplicates().reset_index(drop=True)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Category"] = df["Category"].astype(str).str.strip().str.title()
    df["Type"] = df["Type"].astype(str).str.strip().str.title()
    df["Payment Method"] = df["Payment Method"].astype(str).str.strip().str.title()
    df["Description"] = df["Description"].astype(str).str.strip()
    df["Merchant"] = df["Merchant"].astype(str).str.strip()
    df = df.dropna(subset=["Date", "Amount", "Category", "Type"])

    df["Month"] = df["Date"].dt.month_name()
    df["Year"] = df["Date"].dt.year
    df["Month_Num"] = df["Date"].dt.month
    df["Weekday"] = df["Date"].dt.day_name()
    df["Direction"] = df["Type"].apply(lambda x: "Inflow" if x.lower() == "income" else "Outflow")

    return df


def net_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return the main financial summary for the dataset."""
    totals = df.groupby("Type")["Amount"].sum().reset_index()
    totals["Amount"] = totals["Amount"].round(2)
    net = totals[totals["Type"] == "Income"]["Amount"].sum() - totals[totals["Type"] == "Expense"]["Amount"].sum()
    summary = pd.DataFrame(
        [
            {"Metric": "Total Income", "Value": totals[totals["Type"] == "Income"]["Amount"].sum()},
            {"Metric": "Total Expense", "Value": totals[totals["Type"] == "Expense"]["Amount"].sum()},
            {"Metric": "Net Savings", "Value": net},
        ]
    )
    summary["Value"] = summary["Value"].round(2)
    return summary


def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return expense totals by category."""
    expense_df = df[df["Type"] == "Expense"].copy()
    category_totals = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False).reset_index()
    category_totals["Amount"] = category_totals["Amount"].round(2)
    return category_totals


def payment_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return expense totals by payment method."""
    payment_totals = df.groupby("Payment Method")["Amount"].sum().sort_values(ascending=False).reset_index()
    payment_totals["Amount"] = payment_totals["Amount"].round(2)
    return payment_totals


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return totals for each month by transaction type."""
    monthly = df.groupby(["Month_Num", "Month", "Type"])["Amount"].sum().reset_index()
    monthly["Amount"] = monthly["Amount"].round(2)
    monthly = monthly.sort_values(["Month_Num", "Type"])
    return monthly


def weekday_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return the number of transactions by weekday."""
    weekday_counts = df["Weekday"].value_counts().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    ).reset_index()
    weekday_counts.columns = ["Weekday", "Transactions"]
    return weekday_counts


def overspending_summary(df: pd.DataFrame, budgets: dict = None) -> pd.DataFrame:
    """Compare monthly category spending against a budget dictionary."""
    budgets = budgets or DEFAULT_BUDGETS
    expense_df = df[df["Type"] == "Expense"].copy()
    monthly_category = (
        expense_df.groupby(["Month", "Category"])["Amount"].sum().reset_index()
    )
    monthly_category["Budget"] = monthly_category["Category"].map(budgets)
    monthly_category["Overspent"] = monthly_category["Amount"] > monthly_category["Budget"]
    monthly_category["Amount"] = monthly_category["Amount"].round(2)
    monthly_category["Budget"] = monthly_category["Budget"].round(2)
    return monthly_category.sort_values(["Month", "Category"])


def create_visualizations(df: pd.DataFrame, output_dir: str | Path) -> dict:
    """Create charts, save them to disk, and return saved paths."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    charts = {}
    expense_df = df[df["Type"] == "Expense"].copy()
    category_totals = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    payment_totals = df.groupby("Payment Method")["Amount"].sum().sort_values(ascending=False)
    monthly = df.groupby(["Month_Num", "Type"])["Amount"].sum().unstack(fill_value=0).sort_index()
    pivot_table = expense_df.pivot_table(index="Category", columns="Month", values="Amount", aggfunc="sum", fill_value=0)

    plt.figure(figsize=(10, 5))
    categories = category_totals.index.tolist()
    amounts = category_totals.values
    plt.bar(categories, amounts, color=plt.cm.Spectral(np.linspace(0, 1, len(categories))))
    plt.title("Total Expense by Category")
    plt.xticks(rotation=40, ha="right")
    plt.ylabel("Amount")
    plt.xlabel("Category")
    plt.tight_layout()
    chart_path = output_dir / "category_spending.png"
    plt.savefig(chart_path, dpi=200)
    charts["category_spending"] = str(chart_path)
    plt.close()

    plt.figure(figsize=(8, 8))
    plt.pie(category_totals.values, labels=category_totals.index, autopct="%1.1f%%", startangle=140, textprops={"fontsize": 8})
    plt.title("Expense Distribution by Category")
    plt.axis("equal")
    chart_path = output_dir / "expense_distribution_pie.png"
    plt.savefig(chart_path, dpi=200)
    charts["expense_distribution_pie"] = str(chart_path)
    plt.close()

    plt.figure(figsize=(10, 5))
    monthly.plot(marker="o", linewidth=2)
    plt.title("Monthly Income vs Expense")
    plt.xlabel("Month Number")
    plt.ylabel("Amount")
    plt.grid(True, alpha=0.35)
    plt.legend(title="Type")
    plt.tight_layout()
    chart_path = output_dir / "monthly_income_expense.png"
    plt.savefig(chart_path, dpi=200)
    charts["monthly_income_expense"] = str(chart_path)
    plt.close()

    plt.figure(figsize=(10, 6))
    payment_totals.plot(kind="bar", color="#4C72B0")
    plt.title("Spending by Payment Method")
    plt.xlabel("Payment Method")
    plt.ylabel("Amount")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    chart_path = output_dir / "payment_method_spending.png"
    plt.savefig(chart_path, dpi=200)
    charts["payment_method_spending"] = str(chart_path)
    plt.close()

    plt.figure(figsize=(12, 8))
    pivot_table = pivot_table[sorted(pivot_table.columns, key=lambda x: pd.to_datetime(x, format="%B", errors="coerce").month if isinstance(x, str) else x)]
    sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap="YlOrBr", linewidths=0.5)
    plt.title("Monthly Expense Heatmap by Category")
    plt.ylabel("Category")
    plt.xlabel("Month")
    plt.tight_layout()
    chart_path = output_dir / "expense_heatmap.png"
    plt.savefig(chart_path, dpi=200)
    charts["expense_heatmap"] = str(chart_path)
    plt.close()

    return charts


def save_dataframe(df: pd.DataFrame, path: str | Path) -> None:
    """Save a DataFrame to disk as CSV."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def build_text_report(df: pd.DataFrame, output_dir: str | Path) -> Path:
    """Write a small summary text report."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "summary_report.txt"

    summary_table = net_summary(df)
    category_table = category_summary(df).head(8)
    monthly_table = monthly_summary(df)
    overspend = overspending_summary(df).query("Overspent == True")

    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write("Expense Tracker App Summary\n")
        handle.write("===========================\n\n")
        handle.write("Top-level Metrics:\n")
        handle.write(summary_table.to_string(index=False))
        handle.write("\n\nTop Expense Categories:\n")
        handle.write(category_table.to_string(index=False))
        handle.write("\n\nMonthly Summary:\n")
        handle.write(monthly_table.to_string(index=False))
        handle.write("\n\nOverspending Alerts:\n")
        if overspend.empty:
            handle.write("No categories exceeded the sample budget in this time range.\n")
        else:
            handle.write(overspend.to_string(index=False))

    return report_path
