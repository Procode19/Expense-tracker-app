import streamlit as st
import pandas as pd
from pathlib import Path

from src.expense_tracker import clean_expense_data, generate_synthetic_expense_data

DATA_PATH = Path("data/cleaned_expenses.csv")


@st.cache_data
def load_data() -> pd.DataFrame:
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
    else:
        df = generate_synthetic_expense_data(num_records=300)
        df = clean_expense_data(df)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    selected_categories = st.sidebar.multiselect("Select categories", options=sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
    selected_payment = st.sidebar.multiselect("Select payment methods", options=sorted(df["Payment Method"].unique()), default=sorted(df["Payment Method"].unique()))
    selected_type = st.sidebar.multiselect("Select transaction types", options=sorted(df["Type"].unique()), default=sorted(df["Type"].unique()))
    selected_months = st.sidebar.multiselect("Select months", options=df["Month"].unique(), default=df["Month"].unique())

    filtered = df[
        (df["Category"].isin(selected_categories))
        & (df["Payment Method"].isin(selected_payment))
        & (df["Type"].isin(selected_type))
        & (df["Month"].isin(selected_months))
    ]
    return filtered


def main() -> None:
    st.set_page_config(page_title="Expense Tracker Dashboard", layout="wide")
    st.title("💰 Expense Tracker App")
    st.markdown(
        "Use this dashboard to explore synthetic expense data, visualize category spend, and compare income vs expense trends."
    )

    df = load_data()
    filtered_df = filter_dataframe(df)

    total_income = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
    total_expense = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()
    net_value = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{total_income:,.2f}")
    col2.metric("Total Expense", f"₹{total_expense:,.2f}")
    col3.metric("Net Savings", f"₹{net_value:,.2f}")

    st.subheader("Filtered Transactions")
    st.dataframe(filtered_df.sort_values(by="Date", ascending=False).reset_index(drop=True))

    st.subheader("Category-wise Total Spend")
    category_totals = (
        filtered_df[filtered_df["Type"] == "Expense"].groupby("Category")["Amount"].sum().sort_values(ascending=False)
    )
    st.bar_chart(category_totals)

    st.subheader("Monthly Income vs Expense Trend")
    monthly = filtered_df.groupby(["Month_Num", "Type"])["Amount"].sum().unstack(fill_value=0).sort_index()
    st.line_chart(monthly)

    if "Expense" in filtered_df["Type"].unique():
        st.subheader("Expense Distribution by Category")
        expense_breakdown = filtered_df[filtered_df["Type"] == "Expense"].groupby("Category")["Amount"].sum().sort_values(ascending=False)
        st.bar_chart(expense_breakdown)

    st.sidebar.markdown("---")
    st.sidebar.markdown("Built for students and internship-ready portfolios.")


if __name__ == "__main__":
    main()
