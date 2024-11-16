-- Which countries are currently operated in and which country now has the most physical stores?

SELECT 
    country_code,
    COUNT(country_code) AS total_no_stores
FROM 
    dim_store_details
GROUP BY 
    country_code
ORDER BY 
    total_no_stores DESC;

-- Output:
/*
"country_code"	"total_no_stores"
"GB"	               264
"DE"	               139
"US"	                33
*/