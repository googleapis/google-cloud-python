WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `float64_col`,
    `int64_col`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    STRUCT(
      `bool_col` AS bool_col,
      `int64_col` AS int64_col,
      `float64_col` AS float64_col,
      `string_col` AS string_col
    ) AS `bfcol_4`
  FROM `bfcte_0`
)
SELECT
  `bfcol_4` AS `result_col`
FROM `bfcte_1`