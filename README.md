# Expense Tracker App

## Overview
A beginner-friendly, industry-oriented Expense Tracker App built using synthetic data, Python, and data science tools. The project helps users track expenses, categorize spends, analyze monthly trends, and generate visual insights for budgeting decisions.

## Why this project matters
Expense tracking is a core feature in FinTech, personal finance, banking and business analytics. This project is designed for students who want a polished GitHub portfolio item demonstrating:
- data generation and cleaning
- exploratory data analysis (EDA)
- category and trend reporting
- financial insights and budgets
- dashboard-style presentation with Streamlit

## Features
- Synthetic expense data generation
- Data cleaning and transformation
- Category-wise spending analysis
- Monthly income vs expense trend analysis
- Payment method breakdown
- Overspending alerts against sample budgets
- Visualizations saved as chart images
- Streamlit dashboard for interactive presentation

## Tech stack
- Python 3.x
- pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Optional: Plotly

## Project structure
Expense-Tracker-App/
├── data/                  # Raw and cleaned CSV files
├── notebooks/             # Example notebook for exploratory work
├── outputs/               # Generated charts and text reports
├── src/                   # Reusable Python modules
├── images/                # Screenshots or dashboard images for README
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── main.py                # Main script to generate, clean, analyze, and save results
├── app.py                 # Streamlit dashboard app
└── .gitignore             # Ignore generated files and environment artifacts

## Installation guide
### 1. Install Python
- Download Python 3.10 or newer from https://www.python.org/downloads/
- Verify installation:
  ```bash
  python --version
  ```

### 2. Create a virtual environment
#### Windows
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
#### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## How to run the project
### Run the analysis script
```bash
python main.py
```
This will generate:
- `data/synthetic_expenses.csv`
- `data/cleaned_expenses.csv`
- charts in `outputs/`
- a `outputs/summary_report.txt`

### Run the Streamlit dashboard
```bash
streamlit run app.py
```

## Expected outputs
- A cleaned expense dataset ready for analysis
- Category-wise spending bar chart
- Expense distribution pie chart
- Monthly income vs expense trend chart
- Payment method breakdown chart
- Heatmap of category spending by month
- A short text summary report

## Virtual simulation
This project uses synthetic expense records with categories such as Food, Travel, Rent, Shopping, Bills, and Salary. It simulates realistic payment methods and spending behavior over several months.

### What to capture as proof
- Dataset preview while running `main.py`
- Charts saved in `outputs/`
- Streamlit dashboard running in the browser
- `outputs/summary_report.txt`
- GitHub commit history and final repository link

## GitHub upload steps
1. Create a new repository named `expense-tracker-app`.
2. Add files:
   ```bash
   git init
   git add .
   git commit -m "Initial expense tracker app project"
   git branch -M main
   git remote add origin https://github.com/<username>/expense-tracker-app.git
   git push -u origin main
   ```
3. Use a strong repo description:
   `Expense Tracker App with synthetic data, EDA, visualization, and Streamlit dashboard.`
4. Add tags: `python`, `data-science`, `fintech`, `expense-tracker`, `streamlit`, `portfolio`.

## Future improvements
- add real CSV/Excel upload input
- support monthly budget alerts and recommendations
- build a mobile-friendly web app
- add predictive spend forecasting
- connect to live bank transaction data safely

## Troubleshooting
- If `ModuleNotFoundError: No module named 'src'` occurs, run from the project root.
- If Streamlit fails to start, make sure the virtual environment is activated and dependencies are installed.
- If charts do not save, verify `outputs/` exists and has write permissions.

## Project story for interviews
This project demonstrates the full data science workflow:
1. synthetic dataset creation
2. data cleaning and feature engineering
3. exploratory analysis and visualization
4. dashboard delivery with Streamlit
5. documentation and GitHub-ready structure
