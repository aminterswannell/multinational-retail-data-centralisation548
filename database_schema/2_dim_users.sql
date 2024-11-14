-- Casting columns of dim_users table to required data types shown in table below.
/*
+----------------+--------------------+--------------------+
| dim_users      | current data type  | required data type |
+----------------+--------------------+--------------------+
| first_name     | TEXT               | VARCHAR(255)       |
| last_name      | TEXT               | VARCHAR(255)       |
| date_of_birth  | TEXT               | DATE               |
| country_code   | TEXT               | VARCHAR(?)         |
| user_uuid      | TEXT               | UUID               |
| join_date      | TEXT               | DATE               |
+----------------+--------------------+--------------------+
*/

-- Finding max length of country code 

SELECT
    MAX(LENGTH(country_code)) AS max_length_country_code
    FROM dim_users;

-- max_length_country_code is 3

-- Altering data types to desired

ALTER TABLE dim_users
    ALTER COLUMN first_name TYPE VARCHAR(255),
    ALTER COLUMN last_name TYPE VARCHAR(255),
    ALTER COLUMN date_of_birth TYPE DATE USING CAST(date_of_birth AS DATE),
    ALTER COLUMN country_code TYPE VARCHAR(3),
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
    ALTER COLUMN join_date TYPE DATE USING CAST(join_date AS DATE);