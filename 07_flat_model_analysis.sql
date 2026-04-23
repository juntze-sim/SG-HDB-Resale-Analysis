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
