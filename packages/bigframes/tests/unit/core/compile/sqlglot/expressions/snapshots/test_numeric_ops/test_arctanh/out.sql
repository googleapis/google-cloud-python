SELECT
  CASE
    WHEN ABS(`float64_col`) < 1
    THEN ATANH(`float64_col`)
    WHEN ABS(`float64_col`) > 1
    THEN CAST('NaN' AS FLOAT64)
    ELSE CAST('Infinity' AS FLOAT64) * `float64_col`
  END AS `float64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`