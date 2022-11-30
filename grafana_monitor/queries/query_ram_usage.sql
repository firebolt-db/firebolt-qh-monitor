SELECT
    TO_UNIXTIME(DATE_TRUNC('MINUTE', start_time)) AS "time",
    AVG(total_ram_consumed) AS "AvgPeakRAM",
    MAX(total_ram_consumed) AS "MaxPeakRAM",
    APPROX_PERCENTILE(total_ram_consumed, 0.99) AS "NinetethPercentileRAM",
    MEDIAN(total_ram_consumed) AS "MedianRAM"
FROM information_schema.query_history
WHERE "status" NOT IN ('STARTED_EXECUTION', 'PARSE_ERROR')
    AND start_time >= '${__from:date:iso}'
    AND start_time < '${__to:date:iso}'
GROUP BY DATE_TRUNC('MINUTE', start_time)
ORDER BY "time";
