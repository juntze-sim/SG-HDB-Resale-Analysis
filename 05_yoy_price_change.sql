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
