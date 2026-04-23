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
