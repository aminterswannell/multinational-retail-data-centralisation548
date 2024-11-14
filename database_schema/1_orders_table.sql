-- Casting columns of orders_table to correct data types shown in table below:
/* 
+------------------+--------------------+--------------------+
|   orders_table   | current data type  | required data type |
+------------------+--------------------+--------------------+
| date_uuid        | TEXT               | UUID               |
| user_uuid        | TEXT               | UUID               |
| card_number      | TEXT               | VARCHAR(?)         |
| store_code       | TEXT               | VARCHAR(?)         |
| product_code     | TEXT               | VARCHAR(?)         |
| product_quantity | BIGINT             | SMALLINT           |
+------------------+--------------------+--------------------+
*/

-- Finding max lengths of selected variables.

SELECT 
    MAX(LENGTH(card_number)) AS max_length_card_number,
    MAX(LENGTH(store_code)) AS max_length_store_code,
    MAX(LENGTH(product_code)) AS max_length_product_code
    
FROM orders_table;

-- max_length_card_number is 19
-- max_length_store_code is 12
-- max_length_product_code is 11

-- Altering data types to desired.

ALTER TABLE orders_table
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID,
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
    ALTER COLUMN card_number TYPE VARCHAR(19),
    ALTER COLUMN store_code TYPE VARCHAR(12),
    ALTER COLUMN product_code TYPE VARCHAR(11),
    ALTER COLUMN product_quantity TYPE SMALLINT;