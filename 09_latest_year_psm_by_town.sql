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
