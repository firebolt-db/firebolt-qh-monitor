SELECT COUNT(CASE WHEN "status" = 'STARTED_EXECUTION' THEN 1 ELSE NULL END) AS "Queries Started"
, COUNT(CASE WHEN "status" = 'ENDED_SUCCESSFULLY' THEN 1 ELSE NULL END) AS "Successfully Completed"
, COUNT(CASE WHEN "status" = 'EXECUTION_ERROR' THEN 1 ELSE NULL END) AS "Errors"
, COUNT(CASE WHEN "status" = 'EXECUTION_ERROR' THEN 1 ELSE NULL END) / COUNT(CASE WHEN "status" = 'STARTED_EXECUTION' THEN 1 ELSE NULL END)::DOUBLE AS "Error Rate"
, COUNT(CASE WHEN "status" = 'CANCELED_EXECUTION' THEN 1 ELSE NULL END) AS "Canceled Queries"
, COUNT(CASE WHEN "status" = 'PARSE_ERROR' THEN 1 ELSE NULL END) AS "Parse Errors"
, COUNT(CASE WHEN "status" != 'STARTED_EXECUTION' AND scanned_bytes_storage > 0 THEN 1 ELSE NULL END) AS "Cold Queries"
, COUNT(CASE WHEN "status" != 'STARTED_EXECUTION' AND scanned_bytes_storage > 0 THEN 1 ELSE NULL END) / COUNT(CASE WHEN "status" != 'STARTED_EXECUTION' AND scanned_bytes_storage = 0 THEN 1 ELSE NULL END)::DOUBLE AS "Cold Query Percentage"
FROM information_schema.query_history;
WHERE start_time >= '${__from:date:iso}'
AND start_time < '${__to:date:iso}';
