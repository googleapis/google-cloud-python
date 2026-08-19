SELECT
  IF(`float64_col` > 709.78, CAST('Infinity' AS FLOAT64), EXP(`float64_col`) - 1) AS `float64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`