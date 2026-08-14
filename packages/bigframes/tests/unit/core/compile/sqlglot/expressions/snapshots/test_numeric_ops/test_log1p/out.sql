SELECT
  CASE
    WHEN `float64_col` IS NULL
    THEN NULL
    WHEN `float64_col` > -1
    THEN LN(1 + `float64_col`)
    WHEN `float64_col` < -1
    THEN CAST('NaN' AS FLOAT64)
    ELSE CAST('-Infinity' AS FLOAT64)
  END AS `float64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`