WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `int64_col` AS `bfcol_1`,
    `float64_col` AS `bfcol_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    IF(`bfcol_0`, `bfcol_1`, `bfcol_2`) AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_3` AS `result_col`
FROM `bfcte_1`