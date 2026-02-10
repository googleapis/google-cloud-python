SELECT
  CASE
    WHEN `float64_col` < 1
    THEN CAST('NaN' AS FLOAT64)
    ELSE ACOSH(`float64_col`)
  END AS `float64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`