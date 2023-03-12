SELECT start_date, end_date FROM prices GROUP BY 1, 2 HAVING SUM(price) > 186000;
