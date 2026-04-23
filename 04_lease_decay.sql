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
