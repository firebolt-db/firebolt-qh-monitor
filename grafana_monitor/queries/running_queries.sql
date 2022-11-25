SELECT query_id
, query_text
, start_time
, duration_usec
, inserted_bytes
, inserted_rows
, scanned_bytes
, scanned_rows
FROM information_schema.running_queries
ORDER BY start_time ;
