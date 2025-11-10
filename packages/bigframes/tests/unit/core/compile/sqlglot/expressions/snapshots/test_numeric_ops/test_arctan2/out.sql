WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `int64_col` AS `bfcol_1`,
    `float64_col` AS `bfcol_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    ATAN2(`bfcol_1`, `bfcol_2`) AS `bfcol_6`,
    ATAN2(CAST(`bfcol_0` AS INT64), `bfcol_2`) AS `bfcol_7`
  FROM `bfcte_0`
)
SELECT
  `bfcol_6` AS `int64_col`,
  `bfcol_7` AS `bool_col`
FROM `bfcte_1`