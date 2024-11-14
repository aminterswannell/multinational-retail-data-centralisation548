-- Merging two latitude columns into one and setting data types to required as shown in table below:

/*
+---------------------+-------------------+------------------------+
| store_details_table | current data type |   required data type   |
+---------------------+-------------------+------------------------+
| longitude           | TEXT              | NUMERIC                |
| locality            | TEXT              | VARCHAR(255)           |
| store_code          | TEXT              | VARCHAR(?)             |
| staff_numbers       | TEXT              | SMALLINT               |
| opening_date        | TEXT              | DATE                   |
| store_type          | TEXT              | VARCHAR(255) NULLABLE  |
| latitude            | TEXT              | NUMERIC                |
| country_code        | TEXT              | VARCHAR(?)             |
| continent           | TEXT              | VARCHAR(255)           |
+---------------------+-------------------+------------------------+
*/

-- Finding max length of store_code and country_code

SELECT 
    MAX(LENGTH(store_code)) AS max_store_code_length,
    MAX(LENGTH(country_code)) AS max_country_code_length
    FROM dim_store_details;

-- max_store_code_length is 12
-- max_country_code_length is 2

-- Altering data types to desired

ALTER TABLE dim_store_details
    ALTER COLUMN longitude TYPE FLOAT USING CAST(longitude AS FLOAT),
    ALTER COLUMN locality TYPE VARCHAR(255),
    ALTER COLUMN store_code TYPE VARCHAR(12),
    ALTER COLUMN staff_numbers TYPE SMALLINT,
    ALTER COLUMN opening_date TYPE DATE USING CAST(opening_date AS DATE),
    ALTER COLUMN store_type TYPE VARCHAR(255),
    ALTER COLUMN latitude TYPE FLOAT USING CAST(latitude AS FLOAT),
    ALTER COLUMN country_code TYPE VARCHAR(2),
    ALTER COLUMN continent TYPE VARCHAR(255);