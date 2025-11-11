WITH `bfcte_0` AS (
  SELECT
    `float64_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    COALESCE(`int64_col` IN (1, 2, 3), FALSE) AS `bfcol_2`,
    (
      `int64_col` IS NULL
    ) OR `int64_col` IN (123456) AS `bfcol_3`,
    COALESCE(`int64_col` IN (1.0, 2.0, 3.0), FALSE) AS `bfcol_4`,
    FALSE AS `bfcol_5`,
    COALESCE(`int64_col` IN (2.5, 3), FALSE) AS `bfcol_6`,
    FALSE AS `bfcol_7`,
    COALESCE(`int64_col` IN (123456), FALSE) AS `bfcol_8`,
    (
      `float64_col` IS NULL
    ) OR `float64_col` IN (1, 2, 3) AS `bfcol_9`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `ints`,
  `bfcol_3` AS `ints_w_null`,
  `bfcol_4` AS `floats`,
  `bfcol_5` AS `strings`,
  `bfcol_6` AS `mixed`,
  `bfcol_7` AS `empty`,
  `bfcol_8` AS `ints_wo_match_nulls`,
  `bfcol_9` AS `float_in_ints`
FROM `bfcte_1`