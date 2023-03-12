SELECT EXTRACT(MONTH FROM sale_date) as sale_date, product_id as count FROM sales WHERE sale_date BETWEEN '2020-01-01' and '2020-12-31'GROUP BY sale_date, product_id;

