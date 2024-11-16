-- Find which months in which years have had the most sales historically.

SELECT ROUND(
        SUM(product_quantity * dim_products.product_price)
    ) AS total_sales,
    dim_date_times.year AS year,
    dim_date_times.month AS month
FROM orders_table
    LEFT JOIN dim_products ON orders_table.product_code = dim_products.product_code
    LEFT JOIN dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
GROUP BY month,
    year
ORDER BY total_sales DESC
LIMIT 10;

-- Output:
/*
"total_sales"	"year"	"month"
27937	        "1994"	  "3"
27356	        "2019"	  "1"
27092	        "2009"	  "8"
26680	        "1997"	 "11"
26311	        "2018"	 "12"
26278	        "2019"	  "8"
26237	        "2017"	  "9"
25798	        "2010"	  "5"
25648	        "1996"	  "8"
25615	        "2000"	  "1"
*/