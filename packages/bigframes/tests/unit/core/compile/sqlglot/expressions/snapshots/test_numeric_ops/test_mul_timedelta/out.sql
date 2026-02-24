SELECT
  `rowindex`,
  `timestamp_col`,
  `int64_col`,
  `duration_col`,
  CAST(IF(
    `duration_col` * `int64_col` > 0,
    FLOOR(`duration_col` * `int64_col`),
    CEIL(`duration_col` * `int64_col`)
  ) AS INT64) AS `timedelta_mul_numeric`,
  CAST(IF(
    `int64_col` * `duration_col` > 0,
    FLOOR(`int64_col` * `duration_col`),
    CEIL(`int64_col` * `duration_col`)
  ) AS INT64) AS `numeric_mul_timedelta`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`