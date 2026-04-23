# Singapore HDB Resale Price Analysis (2017–2026)

An end-to-end data analysis project exploring 229,000+ HDB resale flat transactions in Singapore. Built to demonstrate **SQL querying**, **data wrangling**, and **Tableau visualisation** skills.

## Project Overview

Singapore's public housing market is one of the most data-rich and policy-driven real estate markets in the world. This project uses the official HDB resale flat prices dataset from [data.gov.sg](https://data.gov.sg) to answer key questions buyers, analysts, and policymakers care about:

- **How have resale prices trended over the past 9 years?**
- **Which towns are the most (and least) expensive per square metre?**
- **How much of a premium do higher floors command?**
- **Does remaining lease length significantly affect pricing?**
- **Which flat types and flat models hold value best?**

## Data Source

| Field | Detail |
|-------|--------|
| Source | [data.gov.sg — HDB Resale Flat Prices](https://data.gov.sg/datasets/d_8b84c4ee58e3cfc0ece0d773c8ca6abc/view) |
| Period | January 2017 – April 2026 |
| Records | 229,146 transactions |
| Columns | month, town, flat_type, block, street_name, storey_range, floor_area_sqm, flat_model, lease_commence_date, remaining_lease, resale_price |

## Repository Structure

```
sg-hdb-resale-analysis/
├── data/
│   └── hdb_resale_prices.csv          # Raw dataset
├── sql_queries/
│   ├── 01_monthly_price_trends.sql    # Price trends over time by flat type
│   ├── 02_town_comparison.sql         # Town-level price & price/sqm comparison
│   ├── 03_storey_premium.sql          # Higher-floor premium analysis
│   ├── 04_lease_decay.sql             # Remaining lease vs price relationship
│   ├── 05_yoy_price_change.sql        # Year-over-year appreciation by town
│   ├── 06_top_transactions.sql        # Top 10 most expensive sales per year
│   ├── 07_flat_model_analysis.sql     # Pricing by flat model (DBSS, Improved, etc.)
│   ├── 08_monthly_volume.sql          # Transaction volume as market activity proxy
│   ├── 09_latest_year_psm_by_town.sql # 2025 price/sqm distribution by town
│   └── 10_new_vs_old_lease.sql        # New-build vs older flat pricing gap
├── dashboard/
│   └── *.csv                          # Query results exported for Tableau
├── load_and_query.py                  # Pipeline: CSV → SQLite → SQL → CSV exports
├── findings.md                        # Key insights from the analysis
└── README.md
```

## SQL Queries & Business Questions

| # | Query | Business Question |
|---|-------|-------------------|
| 01 | Monthly Price Trends | How have prices moved month-by-month for each flat type? |
| 02 | Town Comparison | Which towns are most/least expensive per sqm? |
| 03 | Storey Premium | How much more do higher floors cost? |
| 04 | Lease Decay | How does remaining lease affect price per sqm? |
| 05 | YoY Price Change | Which towns appreciated fastest year-over-year? |
| 06 | Top Transactions | What were the record-breaking sales each year? |
| 07 | Flat Model Analysis | How do DBSS, Improved, Premium, etc. compare? |
| 08 | Monthly Volume | Is the market heating up or cooling down? |
| 09 | 2025 Price/sqm Distribution | What does the current price spread look like by town? |
| 10 | New vs Old Lease | How big is the pricing gap by lease era? |

## Key Findings

- **Central Area** leads at **S$8,259/sqm** on average — roughly 50% above non-mature estates.
- **Storey premiums** are non-linear: floors 25+ add 20–30% over ground-level units.
- **Lease decay** accelerates sharply below 60 years remaining, reflecting buyer caution and lending restrictions.
- The **highest recorded sale in 2025** was a 5-ROOM in Queenstown at **S$1,658,888**.
- Post-COVID pricing surge (2021–2023) has moderated but prices remain at elevated levels.

See [`findings.md`](findings.md) for the full write-up.

## How to Run

### Prerequisites
- Python 3.8+
- No external packages required (uses built-in `sqlite3` and `csv` modules)

### Steps

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/sg-hdb-resale-analysis.git
cd sg-hdb-resale-analysis

# Run the pipeline (loads CSV into SQLite, runs all queries, exports CSVs)
python load_and_query.py

# Query the database directly
sqlite3 data/hdb_resale.db "SELECT town, ROUND(AVG(resale_price)) FROM resale_transactions GROUP BY town ORDER BY 2 DESC LIMIT 10;"
```

### Tableau
Import any CSV from the `dashboard/` folder into Tableau Public or Tableau Desktop to build visualisations.

## Suggested Tableau Dashboards

1. **Price Trends Dashboard** — Line chart of monthly average prices by flat type (use `01_monthly_price_trends.csv`)
2. **Town Heatmap** — Filled map or bar chart of price/sqm by town (use `02_town_comparison.csv`)
3. **Storey Premium Matrix** — Heatmap of price/sqm by storey range and flat type (use `03_storey_premium.csv`)
4. **Lease Decay Curve** — Scatter plot of remaining lease vs price/sqm (use `04_lease_decay.csv`)
5. **Market Pulse** — Dual-axis chart of monthly volume + average price (use `08_monthly_volume.csv`)

## Tools & Technologies

- **SQLite** — Lightweight database for querying 229K+ rows
- **Python** — Data pipeline (CSV → SQLite → query → export)
- **SQL** — Window functions, CTEs, aggregations, conditional grouping
- **Tableau** — Planned dashboards for visual storytelling

## License

This project uses publicly available data from [data.gov.sg](https://data.gov.sg) under the [Singapore Open Data Licence](https://data.gov.sg/open-data-licence).
