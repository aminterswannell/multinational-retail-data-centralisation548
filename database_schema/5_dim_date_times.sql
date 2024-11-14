-- Casting data types of dim_date_times table to desired in table below:

/*
+-----------------+-------------------+--------------------+
| dim_date_times  | current data type | required data type |
+-----------------+-------------------+--------------------+
| month           | TEXT              | VARCHAR(?)         |
| year            | TEXT              | VARCHAR(?)         |
| day             | TEXT              | VARCHAR(?)         |
| time_period     | TEXT              | VARCHAR(?)         |
| date_uuid       | TEXT              | UUID               |
+-----------------+-------------------+--------------------+
*/

-- Finding max lengths of month, year, day and time_period

SELECT 
    MAX(LENGTH(CAST(year AS VARCHAR))) AS max_year_length,
    MAX(LENGTH(CAST(month AS VARCHAR))) AS max_month_length,
    MAX(LENGTH(CAST(day AS VARCHAR))) AS max_day_length,
    MAX(LENGTH(CAST(time_period AS VARCHAR))) AS max_time_period_length
FROM 
    dim_date_times;

-- max_month_length is 2
-- max_year_length is 4
-- max_day_length is 2
-- max_time_period_length is 10

-- Altering data types to desired

ALTER TABLE dim_date_times
    ALTER COLUMN month TYPE VARCHAR(2),
    ALTER COLUMN year TYPE VARCHAR(4),
    ALTER COLUMN day TYPE VARCHAR(2),
    ALTER COLUMN time_period TYPE VARCHAR(10),
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;