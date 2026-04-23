-- Monthly transaction volume — a proxy for market activity
-- Use: Area chart showing market heat
SELECT
    month,
    COUNT(*)                    AS num_transactions,
    ROUND(AVG(resale_price), 0) AS avg_price
FROM resale_transactions
GROUP BY month
ORDER BY month;
