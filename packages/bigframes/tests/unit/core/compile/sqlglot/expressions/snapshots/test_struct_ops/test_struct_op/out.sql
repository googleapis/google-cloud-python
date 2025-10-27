WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `int64_col` AS `bfcol_1`,
    `float64_col` AS `bfcol_2`,
    `string_col` AS `bfcol_3`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    STRUCT(
      `bfcol_0` AS bool_col,
      `bfcol_1` AS int64_col,
      `bfcol_2` AS float64_col,
      `bfcol_3` AS string_col
    ) AS `bfcol_4`
  FROM `bfcte_0`
)
SELECT
  `bfcol_4` AS `result_col`
FROM `bfcte_1`