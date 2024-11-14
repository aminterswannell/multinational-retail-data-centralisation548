-- Adding primary keys to each 'dim' table to match columns in orders_table

-- Adding primary key to dim_users

ALTER TABLE dim_users
ADD PRIMARY KEY (user_uuid);

-- Adding primary key to dim_store_details

ALTER TABLE dim_store_details
ADD PRIMARY KEY (store_code);

-- Adding primary key to dim_products

ALTER TABLE dim_products
ADD PRIMARY KEY (product_code);

-- Adding primary key to dim_date_times

ALTER TABLE dim_date_times
ADD PRIMARY KEY (date_uuid);

-- Adding primary key to dim_card_details

ALTER TABLE dim_card_details
ADD PRIMARY KEY (card_number);