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
