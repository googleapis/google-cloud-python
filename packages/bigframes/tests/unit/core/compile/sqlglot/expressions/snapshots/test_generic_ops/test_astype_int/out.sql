SELECT
  UNIX_MICROS(CAST(`datetime_col` AS TIMESTAMP)) AS `datetime_col`,
  UNIX_MICROS(SAFE_CAST(`datetime_col` AS TIMESTAMP)) AS `datetime_w_safe`,
  TIME_DIFF(CAST(`time_col` AS TIME), '00:00:00', MICROSECOND) AS `time_col`,
  TIME_DIFF(SAFE_CAST(`time_col` AS TIME), '00:00:00', MICROSECOND) AS `time_w_safe`,
  UNIX_MICROS(`timestamp_col`) AS `timestamp_col`,
  CAST(TRUNC(`numeric_col`) AS INT64) AS `numeric_col`,
  CAST(TRUNC(`float64_col`) AS INT64) AS `float64_col`,
  SAFE_CAST(TRUNC(`float64_col`) AS INT64) AS `float64_w_safe`,
  CAST('100' AS INT64) AS `str_const`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`