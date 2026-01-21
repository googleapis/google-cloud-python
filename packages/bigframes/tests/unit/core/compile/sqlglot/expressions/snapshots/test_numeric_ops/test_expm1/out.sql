WITH `bfcte_0` AS (
  SELECT
    `float64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    IF(`float64_col` > 709.78, CAST('Infinity' AS FLOAT64), EXP(`float64_col`) - 1) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `float64_col`
FROM `bfcte_1`