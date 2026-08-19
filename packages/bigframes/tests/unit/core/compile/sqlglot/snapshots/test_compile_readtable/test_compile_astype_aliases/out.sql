SELECT
  `rowindex`,
  CAST(`timestamp_col` AS STRING) AS `timestamp_col`,
  CAST(`int64_col` AS FLOAT64) AS `int64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
