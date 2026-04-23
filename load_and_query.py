import sqlite3
import csv
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "data", "hdb_resale.db")
CSV_PATH = os.path.join(BASE, "data", "hdb_resale_prices.csv")
SQL_DIR = os.path.join(BASE, "sql_queries")
DASH_DIR = os.path.join(BASE, "dashboard")

# ── 1. Load CSV into SQLite ──────────────────────────────────────────────
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS resale_transactions")
cur.execute("""
CREATE TABLE resale_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT,
    town TEXT,
    flat_type TEXT,
    block TEXT,
    street_name TEXT,
    storey_range TEXT,
    floor_area_sqm REAL,
    flat_model TEXT,
    lease_commence_date INTEGER,
    remaining_lease TEXT,
    resale_price REAL
)
""")

with open(CSV_PATH, "r") as f:
    reader = csv.DictReader(f)
    rows = [(r["month"], r["town"], r["flat_type"], r["block"], r["street_name"],
             r["storey_range"], float(r["floor_area_sqm"]), r["flat_model"],
             int(r["lease_commence_date"]), r["remaining_lease"], float(r["resale_price"]))
            for r in reader]

cur.executemany("""
INSERT INTO resale_transactions
    (month, town, flat_type, block, street_name, storey_range,
     floor_area_sqm, flat_model, lease_commence_date, remaining_lease, resale_price)
VALUES (?,?,?,?,?,?,?,?,?,?,?)
""", rows)
conn.commit()
print(f"Loaded {len(rows):,} rows into SQLite.")

# ── 2. Define & run queries ──────────────────────────────────────────────
queries = {}

# Q1: Monthly price trends by flat type
queries["01_monthly_price_trends"] = """
-- Monthly median & average resale price by flat type
-- Use: Line chart showing price trends over time
SELECT
    month,
    flat_type,
    COUNT(*)                          AS num_transactions,
    ROUND(AVG(resale_price), 0)       AS avg_price,
    ROUND(MIN(resale_price), 0)       AS min_price,
    ROUND(MAX(resale_price), 0)       AS max_price
FROM resale_transactions
GROUP BY month, flat_type
ORDER BY month, flat_type;
"""

# Q2: Town comparison — average PSF and price
queries["02_town_comparison"] = """
-- Average price and price-per-sqm by town (all time)
-- Use: Bar chart / map comparing towns
SELECT
    town,
    COUNT(*)                                        AS num_transactions,
    ROUND(AVG(resale_price), 0)                     AS avg_price,
    ROUND(AVG(resale_price / floor_area_sqm), 2)    AS avg_price_per_sqm,
    ROUND(MIN(resale_price), 0)                     AS min_price,
    ROUND(MAX(resale_price), 0)                     AS max_price
FROM resale_transactions
GROUP BY town
ORDER BY avg_price_per_sqm DESC;
"""

# Q3: Storey premium analysis
queries["03_storey_premium"] = """
-- Average price by storey range for each flat type
-- Use: Heatmap or grouped bar chart showing storey premiums
SELECT
    flat_type,
    storey_range,
    COUNT(*)                                        AS num_transactions,
    ROUND(AVG(resale_price), 0)                     AS avg_price,
    ROUND(AVG(resale_price / floor_area_sqm), 2)    AS avg_price_per_sqm
FROM resale_transactions
GROUP BY flat_type, storey_range
ORDER BY flat_type,
    CAST(SUBSTR(storey_range, 1, INSTR(storey_range, ' ') - 1) AS INTEGER);
"""

# Q4: Lease decay — how remaining lease affects price
queries["04_lease_decay"] = """
-- Price per sqm vs remaining lease years
-- Use: Scatter plot showing lease decay effect
SELECT
    CAST(SUBSTR(remaining_lease, 1, INSTR(remaining_lease, ' ') - 1) AS INTEGER) AS remaining_years,
    flat_type,
    COUNT(*)                                        AS num_transactions,
    ROUND(AVG(resale_price / floor_area_sqm), 2)    AS avg_price_per_sqm,
    ROUND(AVG(resale_price), 0)                     AS avg_price
FROM resale_transactions
WHERE remaining_lease IS NOT NULL AND remaining_lease != ''
GROUP BY remaining_years, flat_type
HAVING num_transactions >= 10
ORDER BY flat_type, remaining_years;
"""

# Q5: Year-over-year price change by town
queries["05_yoy_price_change"] = """
-- Year-over-year average price change by town
-- Use: Heatmap showing which towns appreciated fastest
WITH yearly AS (
    SELECT
        town,
        SUBSTR(month, 1, 4) AS year,
        ROUND(AVG(resale_price), 0) AS avg_price
    FROM resale_transactions
    GROUP BY town, year
)
SELECT
    a.town,
    a.year,
    a.avg_price,
    b.avg_price AS prev_year_price,
    ROUND((a.avg_price - b.avg_price) * 100.0 / b.avg_price, 2) AS yoy_pct_change
FROM yearly a
LEFT JOIN yearly b ON a.town = b.town AND CAST(a.year AS INTEGER) = CAST(b.year AS INTEGER) + 1
ORDER BY a.town, a.year;
"""

# Q6: Top 10 most expensive transactions each year
queries["06_top_transactions"] = """
-- Top 10 most expensive resale transactions per year
-- Use: Table / highlight reel
WITH ranked AS (
    SELECT *,
        SUBSTR(month, 1, 4) AS year,
        ROW_NUMBER() OVER (PARTITION BY SUBSTR(month, 1, 4) ORDER BY resale_price DESC) AS rn
    FROM resale_transactions
)
SELECT year, month, town, flat_type, block, street_name,
       storey_range, floor_area_sqm, flat_model,
       lease_commence_date, resale_price
FROM ranked
WHERE rn <= 10
ORDER BY year DESC, resale_price DESC;
"""

# Q7: Flat model popularity and pricing
queries["07_flat_model_analysis"] = """
-- Transaction volume and pricing by flat model
-- Use: Treemap or bar chart
SELECT
    flat_model,
    COUNT(*)                                        AS num_transactions,
    ROUND(AVG(resale_price), 0)                     AS avg_price,
    ROUND(AVG(resale_price / floor_area_sqm), 2)    AS avg_price_per_sqm,
    ROUND(AVG(floor_area_sqm), 1)                   AS avg_floor_area
FROM resale_transactions
GROUP BY flat_model
ORDER BY num_transactions DESC;
"""

# Q8: Monthly transaction volume
queries["08_monthly_volume"] = """
-- Monthly transaction volume — a proxy for market activity
-- Use: Area chart showing market heat
SELECT
    month,
    COUNT(*)                    AS num_transactions,
    ROUND(AVG(resale_price), 0) AS avg_price
FROM resale_transactions
GROUP BY month
ORDER BY month;
"""

# Q9: Price-per-sqm distribution by town (latest year)
queries["09_latest_year_psm_by_town"] = """
-- Price per sqm by town for the latest full year (2025)
-- Use: Box plot or violin chart in Tableau
SELECT
    town,
    flat_type,
    resale_price,
    floor_area_sqm,
    ROUND(resale_price / floor_area_sqm, 2) AS price_per_sqm,
    storey_range,
    remaining_lease
FROM resale_transactions
WHERE month >= '2025-01' AND month <= '2025-12'
ORDER BY town, price_per_sqm DESC;
"""

# Q10: New vs old lease comparison
queries["10_new_vs_old_lease"] = """
-- Comparing new leases (built after 2010) vs older flats
-- Use: Side-by-side bar chart
SELECT
    CASE
        WHEN lease_commence_date >= 2010 THEN 'New (2010+)'
        WHEN lease_commence_date >= 2000 THEN 'Mid (2000-2009)'
        WHEN lease_commence_date >= 1990 THEN 'Older (1990-1999)'
        ELSE 'Oldest (<1990)'
    END AS lease_era,
    flat_type,
    COUNT(*) AS num_transactions,
    ROUND(AVG(resale_price), 0) AS avg_price,
    ROUND(AVG(resale_price / floor_area_sqm), 2) AS avg_price_per_sqm
FROM resale_transactions
GROUP BY lease_era, flat_type
ORDER BY lease_era, flat_type;
"""

# ── 3. Save SQL files & export CSVs ─────────────────────────────────────
for name, sql in queries.items():
    # Save .sql file
    with open(os.path.join(SQL_DIR, f"{name}.sql"), "w") as f:
        f.write(sql.strip() + "\n")

    # Run query and export CSV
    cur.execute(sql)
    cols = [desc[0] for desc in cur.description]
    rows_out = cur.fetchall()
    csv_path = os.path.join(DASH_DIR, f"{name}.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(rows_out)
    print(f"  {name}: {len(rows_out):,} rows → dashboard/{name}.csv")

conn.close()
print("\nDone! Database at data/hdb_resale.db")
