SELECT  DATE_PART('day', AGE(end_date, start_date)) FROM prices GROUP BY end_date, start_date HAVING  SUM(price) > 186000;

