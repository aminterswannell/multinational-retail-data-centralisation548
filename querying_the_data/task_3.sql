-- Which months have produced the most sales?

SELECT 
    TO_CHAR(SUM(dim_products.product_price * orders_table.product_quantity), 'FM999999.99') AS total_sales,
    dim_date_times.month AS month
FROM 
    orders_table
JOIN 
    dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
JOIN
    dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY 
    month
ORDER BY 
    total_sales DESC
LIMIT 6;

-- Output:
/*
"total_sales"	"month"
"672931.43"	      "8"
"667847.06"	      "1"
"657092.83"	     "10"
"650116.56"	      "5"
"645509.17"  	  "7"
"645303.62"	      "3"
*/