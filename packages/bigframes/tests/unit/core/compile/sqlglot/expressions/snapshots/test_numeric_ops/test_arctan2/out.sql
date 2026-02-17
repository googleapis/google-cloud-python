SELECT
  ATAN2(`int64_col`, `float64_col`) AS `int64_col`,
  ATAN2(CAST(`bool_col` AS INT64), `float64_col`) AS `bool_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`