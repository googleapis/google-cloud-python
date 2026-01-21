WITH `bfcte_0` AS (
  SELECT
    `float64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE
      WHEN `float64_col` IS NULL
      THEN NULL
      WHEN `float64_col` > -1
      THEN LN(1 + `float64_col`)
      WHEN `float64_col` < -1
      THEN CAST('NaN' AS FLOAT64)
      ELSE CAST('-Infinity' AS FLOAT64)
    END AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `float64_col`
FROM `bfcte_1`