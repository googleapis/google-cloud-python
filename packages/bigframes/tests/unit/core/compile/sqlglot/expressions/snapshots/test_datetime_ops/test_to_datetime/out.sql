SELECT
  CAST(TIMESTAMP_MICROS(CAST(TRUNC(`int64_col` * 0.001) AS INT64)) AS DATETIME) AS `int64_col`,
  SAFE_CAST(`string_col` AS DATETIME),
  CAST(TIMESTAMP_MICROS(CAST(TRUNC(`float64_col` * 0.001) AS INT64)) AS DATETIME) AS `float64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`