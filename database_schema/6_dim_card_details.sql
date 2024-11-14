-- Casting data types of dim_card_details table to desired as shown in table below:

/*
+------------------------+-------------------+--------------------+
|    dim_card_details    | current data type | required data type |
+------------------------+-------------------+--------------------+
| card_number            | TEXT              | VARCHAR(?)         |
| expiry_date            | TEXT              | VARCHAR(?)         |
| date_payment_confirmed | TEXT              | DATE               |
+------------------------+-------------------+--------------------+
*/

SELECT 
    MAX(LENGTH(card_number)) AS max_card_number_length, 
    MAX(LENGTH(expiry_date)) AS max_expiry_date_length 
FROM dim_card_details;

-- max_card_number_length is 19
-- max_expiry_date_length is 5

-- Altering data types to desired

ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE VARCHAR(19),
    ALTER COLUMN expiry_date TYPE VARCHAR(5),
    ALTER COLUMN date_payment_confirmed TYPE DATE USING CAST(date_payment_confirmed AS DATE);