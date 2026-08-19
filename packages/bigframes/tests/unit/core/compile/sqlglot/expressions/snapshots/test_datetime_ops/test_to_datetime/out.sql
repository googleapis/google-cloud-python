SELECT
  DATETIME(TIMESTAMP_MICROS(CAST(TRUNC(`int64_col` * 0.001) AS INT64)), 'UTC') AS `int64_col`,
  SAFE_CAST(`string_col` AS DATETIME) AS `string_col`,
  DATETIME(TIMESTAMP_MICROS(CAST(TRUNC(`float64_col` * 0.001) AS INT64)), 'UTC') AS `float64_col`,
  DATETIME(`timestamp_col`, 'UTC') AS `timestamp_col`,
  SAFE_CAST(`string_col` AS DATETIME) AS `string_col_fmt`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
