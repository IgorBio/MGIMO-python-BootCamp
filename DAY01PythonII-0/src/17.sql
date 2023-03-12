SELECT product_id, AVG(price) as avg_price FROM prices WHERE start_date BETWEEN '2020-01-01' and '2020-12-31' GROUP BY 1 ORDER BY 1;
