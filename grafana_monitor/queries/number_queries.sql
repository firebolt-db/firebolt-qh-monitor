SELECT
    engine_name,
    TO_UNIXTIME(DATE_TRUNC('MINUTE', start_time)) AS "time",
    COUNT(*) AS number_queries
FROM information_schema.query_history
WHERE status NOT IN ('STARTED_EXECUTION', 'PARSE_ERROR')
AND start_time >= '${__from:date:iso}'
AND start_time < '${__to:date:iso}'
GROUP BY engine_name, DATE_TRUNC('MINUTE', start_time)
ORDER BY "time";
