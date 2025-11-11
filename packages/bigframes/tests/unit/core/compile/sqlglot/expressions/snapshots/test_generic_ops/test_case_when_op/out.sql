WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `float64_col`,
    `int64_col`,
    `int64_too`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE WHEN `bool_col` THEN `int64_col` END AS `bfcol_4`,
    CASE WHEN `bool_col` THEN `int64_col` WHEN `bool_col` THEN `int64_too` END AS `bfcol_5`,
    CASE WHEN `bool_col` THEN `bool_col` WHEN `bool_col` THEN `bool_col` END AS `bfcol_6`,
    CASE
      WHEN `bool_col`
      THEN `int64_col`
      WHEN `bool_col`
      THEN CAST(`bool_col` AS INT64)
      WHEN `bool_col`
      THEN `float64_col`
    END AS `bfcol_7`
  FROM `bfcte_0`
)
SELECT
  `bfcol_4` AS `single_case`,
  `bfcol_5` AS `double_case`,
  `bfcol_6` AS `bool_types_case`,
  `bfcol_7` AS `mixed_types_cast`
FROM `bfcte_1`