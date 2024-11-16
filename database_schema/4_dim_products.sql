-- Removing £ and creating weight_class column as shown below:

/*
+--------------------------+-------------------+
| weight_class VARCHAR(?)  | weight range(kg)  |
+--------------------------+-------------------+
| Light                    | < 2               |
| Mid_Sized                | >= 2 - < 40       |
| Heavy                    | >= 40 - < 140     |
| Truck_Required           | => 140            |
+----------------------------+-----------------+
*/

UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '');

ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(14);

UPDATE dim_products
SET weight_class = CASE
        WHEN weight_kg < 2.0 THEN 'Light'
        WHEN weight_kg >= 2.0 AND weight_kg < 40.0 THEN 'Mid_Sized'
        WHEN weight_kg >= 40.0 AND weight_kg < 140 THEN 'Heavy'
        WHEN weight_kg >= 140.0 THEN 'Truck_Required'
END;

-- Renaming removed column to still_available and changing data types of table to those shown below

/*
+-----------------+--------------------+--------------------+
|  dim_products   | current data type  | required data type |
+-----------------+--------------------+--------------------+
| product_price   | TEXT               | NUMERIC            |
| weight          | TEXT               | NUMERIC            |
| EAN             | TEXT               | VARCHAR(?)         |
| product_code    | TEXT               | VARCHAR(?)         |
| date_added      | TEXT               | DATE               |
| uuid            | TEXT               | UUID               |
| still_available | TEXT               | BOOL               |
| weight_class    | TEXT               | VARCHAR(?)         |
+-----------------+--------------------+--------------------+
*/

ALTER TABLE dim_products
    RENAME COLUMN removed to still_available;

-- Finding max lengths of EAN and product_code 

SELECT
    MAX(LENGTH("EAN")) AS max_ean_length,
    MAX(LENGTH(product_code)) AS max_product_code_length
FROM dim_products;

-- max_ean_length is 17
-- max_product_code_length is 11

-- Altering data types to desired

ALTER TABLE dim_products
    ALTER COLUMN product_price TYPE FLOAT USING CAST(product_price AS FLOAT),
    ALTER COLUMN weight_kg TYPE FLOAT USING CAST(weight_kg AS FLOAT),
    ALTER COLUMN "EAN" TYPE VARCHAR(17),
    ALTER COLUMN product_code TYPE VARCHAR(11),
    ALTER COLUMN date_added TYPE DATE USING CAST(date_added AS DATE),
    ALTER COLUMN uuid TYPE UUID USING uuid::UUID,
    ALTER COLUMN still_available TYPE BOOL USING(still_available = 'still_avaliable'),
    ALTER COLUMN weight_class TYPE VARCHAR(14);