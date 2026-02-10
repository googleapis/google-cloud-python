SELECT
  `rowindex`,
  `timestamp_col`,
  `int64_col`,
  `duration_col`,
  CAST(FLOOR(`duration_col` * `int64_col`) AS INT64) AS `timedelta_mul_numeric`,
  CAST(FLOOR(`int64_col` * `duration_col`) AS INT64) AS `numeric_mul_timedelta`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`