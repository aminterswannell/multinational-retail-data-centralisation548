-- Determine the staff numbers in each of the countries the company sells in.

SELECT SUM(staff_numbers) AS total_staff_numbers,
    country_code
FROM dim_store_details
GROUP BY country_code
ORDER BY total_staff_numbers DESC;

-- Output:
/*
"total_staff_numbers"	"country_code"
13132	                     "GB"
6054	                     "DE"
1304	                     "US"
*/