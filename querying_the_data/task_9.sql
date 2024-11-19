-- Determine the average time taken between each sale grouped by year.

/* The timestamp column in my table contained a default '1900-01-01' attached to every value,
   so I executed this script to create a new column 'timestamp_fix' which dropped this date:
   ALTER TABLE dim_date_times
   ADD timestamp_fix VARCHAR(8);

   UPDATE dim_date_times
   SET timestamp_fix = (
	TO_CHAR(timestamp, 'HH24:MI:SS') timestamp_fix
    );
    */

-- I then altered my code and flagged this with a # to prevent this from happening when run again.

WITH time_joiner AS(
    SELECT TO_TIMESTAMP(
            (
                year || '-' || month || '-' || day || ' ' || timestamp_fix
            ),
            'YYYY-MM-DD HH24:MI:SS'
        ) as join_date,
        year
    FROM dim_date_times
    ORDER BY join_date DESC
),
time_difference as(
    SELECT year,
        join_date,
        LEAD(join_date, 1) OVER (
            ORDER BY join_date DESC
        ) as time_difference
    FROM time_joiner
)
SELECT year,
    AVG((join_date - time_difference)) AS actual_time_taken
FROM time_difference
GROUP BY year
ORDER BY actual_time_taken DESC
LIMIT 5;

-- Output:
/* 
"year"	"actual_time_taken"
"2013"	"02:17:12.300182"
"1993"	"02:15:35.857327"
"2002"	"02:13:50.412529"
"2022"	"02:13:06.313993"
"2008"	"02:13:02.80308"
*/