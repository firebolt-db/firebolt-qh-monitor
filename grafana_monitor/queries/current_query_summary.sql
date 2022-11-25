SELECT COUNT(*) AS "Number Current Queries"
, max(duration_usec) AS "Longest running query"
FROM information_schema.running_queries;
