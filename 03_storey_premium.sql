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
