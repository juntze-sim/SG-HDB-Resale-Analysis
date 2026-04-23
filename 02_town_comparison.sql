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
