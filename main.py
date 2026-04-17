import streamlit as st
from pathlib import Path

from src.expense_tracker import (
    build_text_report,
    clean_expense_data,
    create_visualizations,
    generate_synthetic_expense_data,
    save_dataframe,
)

st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💰 Expense Tracker Dashboard")

# ---------------- PATH SETUP ----------------
project_root = Path(__file__).parent
data_dir = project_root / "data"
outputs_dir = project_root / "outputs"

data_dir.mkdir(exist_ok=True)
outputs_dir.mkdir(exist_ok=True)

raw_path = data_dir / "synthetic_expenses.csv"
clean_path = data_dir / "cleaned_expenses.csv"

# ---------------- BUTTON ----------------
if st.button("🚀 Generate Expense Data & Analysis"):

    st.write("➡ Generating synthetic expense dataset...")
    df_raw = generate_synthetic_expense_data(num_records=360)
    save_dataframe(df_raw, raw_path)

    st.success("Raw data generated ✅")
    st.dataframe(df_raw.head())

    st.write("➡ Cleaning data...")
    df_clean = clean_expense_data(df_raw)
    save_dataframe(df_clean, clean_path)

    st.success("Cleaned data ready ✅")
    st.dataframe(df_clean.head())

    st.write("➡ Creating visualizations...")
    chart_paths = create_visualizations(df_clean, outputs_dir)

    st.success("Charts created ✅")

    # Display charts
    st.subheader("📊 Visualizations")
    for name, path in chart_paths.items():
        st.image(str(path), caption=name, use_container_width=True)

    # Report
    st.write("➡ Generating report...")
    report_path = build_text_report(df_clean, outputs_dir)

    st.success("Report generated ✅")

    # Show report content
    with open(report_path, "r") as f:
        report_text = f.read()

    st.subheader("📄 Summary Report")
    st.text(report_text)

    st.success("🎉 Expense Tracker Completed Successfully!")