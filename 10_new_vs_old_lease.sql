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
