SELECT
  CASE
    WHEN `float64_col` > 709.78
    THEN CAST('Infinity' AS FLOAT64)
    ELSE EXP(`float64_col`)
  END AS `float64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`