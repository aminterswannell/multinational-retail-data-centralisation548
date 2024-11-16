-- Which locations currently have the most stores?

SELECT 
    locality,
    COUNT(locality) AS total_no_stores
FROM 
    dim_store_details
GROUP BY 
    locality
ORDER BY 
    total_no_stores DESC
LIMIT 7;

-- Output:
/*
"locality"	"total_no_stores"
"Chapletown"	   14
"Belper"	       13
"Bushey"	       12
"Exeter"	       11
"Arbroath"     	   10
"High Wycombe"	   10
"Rutherglen"	   10
*/