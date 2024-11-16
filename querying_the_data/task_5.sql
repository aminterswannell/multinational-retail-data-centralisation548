-- Find out the total revenue coming from each of the different store types and the number of sales made as a percentage.

SELECT dim_store_details.store_type AS store_type,
    ROUND(
        SUM(product_quantity * dim_products.product_price)
    ) AS total_sales,
    ROUND(
        SUM(product_quantity * dim_products.product_price) / (
        SELECT SUM(product_quantity * dim_products.product_price)
        FROM orders_table
            LEFT JOIN dim_products on orders_table.product_code = dim_products.product_code
    ) * 100
    ) AS "percentage_total(%)"
FROM orders_table
    LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
    LEFT JOIN dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY store_type
ORDER BY total_sales DESC;

-- Output:
/*
"store_type"	"total_sales"	"percentage_total(%)"
"Local"	           3413322	       44.218417410819605
"Web Portal"	   1725945	        22.35902301626505
"Super Store"	   1209514	       15.668835666256541
"Mall Kiosk"	   698634	        9.050566097089213
"Outlet"	       607055	        7.864189967790012
*/