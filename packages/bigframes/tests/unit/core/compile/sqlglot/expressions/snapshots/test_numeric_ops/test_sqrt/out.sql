SELECT
  CASE WHEN `float64_col` < 0 THEN CAST('NaN' AS FLOAT64) ELSE SQRT(`float64_col`) END AS `float64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`