SELECT
    engine_name,
    TO_UNIXTIME(DATE_TRUNC('MINUTE', start_time)) AS "time",
    AVG(cpu_usage_us) AS "AvgCPUTime",
    MAX(cpu_usage_us) AS "MaxCPUTime",
    APPROX_PERCENTILE(cpu_usage_us, 0.99) AS "NinetethPercentileCPUTime",
    MEDIAN(cpu_usage_us) AS "MedianCPUTime",
    AVG(cpu_delay_us) AS "AvgCPUDelay",
    MAX(cpu_delay_us) AS "MaxCPUDelay",
    APPROX_PERCENTILE(cpu_delay_us, 0.99) AS "NinetethPercentileCPUDelay",
    MEDIAN(cpu_delay_us) AS "MedianCPUDelay"
FROM information_schema.query_history
WHERE "status" NOT IN ('STARTED_EXECUTION', 'PARSE_ERROR')
    AND start_time >= '${__from:date:iso}'
    AND start_time < '${__to:date:iso}'
GROUP BY DATE_TRUNC('MINUTE', start_time), engine_name
ORDER BY "time";
