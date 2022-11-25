SELECT
    "status" AS "Error Type",
    error_message AS "Error Message",
    start_time AS "Query Start Time"
FROM information_schema.query_history
WHERE error_message != ''
AND start_time >= '${__from:date:iso}'
AND start_time < '${__to:date:iso}'
ORDER BY 3;
