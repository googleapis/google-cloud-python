WITH `bfcte_0` AS (
  SELECT
    `float64_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE WHEN `bfcol_0` < 1 THEN CAST('NaN' AS FLOAT64) ELSE ACOSH(`bfcol_0`) END AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `float64_col`
FROM `bfcte_1`