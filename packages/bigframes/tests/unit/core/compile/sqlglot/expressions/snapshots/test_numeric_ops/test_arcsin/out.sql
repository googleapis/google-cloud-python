SELECT
  CASE
    WHEN ABS(`float64_col`) > 1
    THEN CAST('NaN' AS FLOAT64)
    ELSE ASIN(`float64_col`)
  END AS `float64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`