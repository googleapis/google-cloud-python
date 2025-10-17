WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `int64_col` AS `bfcol_1`,
    `int64_too` AS `bfcol_2`,
    `float64_col` AS `bfcol_3`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE WHEN `bfcol_0` THEN `bfcol_1` END AS `bfcol_4`,
    CASE WHEN `bfcol_0` THEN `bfcol_1` WHEN `bfcol_0` THEN `bfcol_2` END AS `bfcol_5`,
    CASE WHEN `bfcol_0` THEN `bfcol_0` WHEN `bfcol_0` THEN `bfcol_0` END AS `bfcol_6`,
    CASE
      WHEN `bfcol_0`
      THEN `bfcol_1`
      WHEN `bfcol_0`
      THEN CAST(`bfcol_0` AS INT64)
      WHEN `bfcol_0`
      THEN `bfcol_3`
    END AS `bfcol_7`
  FROM `bfcte_0`
)
SELECT
  `bfcol_4` AS `single_case`,
  `bfcol_5` AS `double_case`,
  `bfcol_6` AS `bool_types_case`,
  `bfcol_7` AS `mixed_types_cast`
FROM `bfcte_1`