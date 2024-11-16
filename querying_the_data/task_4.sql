-- Calculate how many products were sold and the amount of sales made for online and offline purchases.

SELECT 
    COUNT(product_quantity) AS number_of_sales,
    SUM(product_quantity) AS product_quantity_count,
    CASE
        WHEN dim_store_details.store_type = 'Web Portal' THEN 'Web'
        ELSE 'Offline'
    END AS location
FROM orders_table
    LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
GROUP BY location
ORDER BY product_quantity_count;

-- Output:
/*
"number_of_sales"	"product_quantity_count"	"location"
26957	                      107739	           "Web"
93166	                      374047           "Offline"
*/