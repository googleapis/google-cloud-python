SELECT
  CAST(TIMESTAMP_MICROS(`int64_col`) AS DATETIME) AS `int64_to_datetime`,
  CAST(TIMESTAMP_MICROS(`int64_col`) AS TIME) AS `int64_to_time`,
  CAST(TIMESTAMP_MICROS(`int64_col`) AS TIMESTAMP) AS `int64_to_timestamp`,
  SAFE_CAST(TIMESTAMP_MICROS(`int64_col`) AS TIME) AS `int64_to_time_safe`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`