
SELECT CASE WHEN scanned_bytes_cache > 0 THEN 'Cold' ELSE 'Warm' END AS "Query Cache Status"
, COUNT(*) AS "Number Queries"
, AVG(duration_usec) AS "Avg Duration"
, MAX(duration_usec) AS "Max Duration"
, MEDIAN(duration_usec) "Median Duration"
, APPROX_PERCENTILE(duration_usec,0.99) "99th Percentile"
, APPROX_PERCENTILE(duration_usec, 0.999) "99.9th Percentile"
FROM information_schema.query_history
WHERE start_time >= '${__from:date:iso}'
AND start_time < '${__to:date:iso}'
AND status != 'STARTED_EXECUTION'
GROUP BY CASE WHEN scanned_bytes_storage > 0 THEN 'Cold' ELSE 'Warm' END;
