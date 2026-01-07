WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `float64_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    COALESCE(`bool_col` IN (TRUE, FALSE), FALSE) AS `bfcol_3`,
    COALESCE(`int64_col` IN (1, 2, 3), FALSE) AS `bfcol_4`,
    `int64_col` IS NULL AS `bfcol_5`,
    COALESCE(`int64_col` IN (1.0, 2.0, 3.0), FALSE) AS `bfcol_6`,
    FALSE AS `bfcol_7`,
    COALESCE(`int64_col` IN (2.5, 3), FALSE) AS `bfcol_8`,
    FALSE AS `bfcol_9`,
    FALSE AS `bfcol_10`,
    COALESCE(`int64_col` IN (123456), FALSE) AS `bfcol_11`,
    (
      `float64_col` IS NULL
    ) OR `float64_col` IN (1, 2, 3) AS `bfcol_12`
  FROM `bfcte_0`
)
SELECT
  `bfcol_3` AS `bools`,
  `bfcol_4` AS `ints`,
  `bfcol_5` AS `ints_w_null`,
  `bfcol_6` AS `floats`,
  `bfcol_7` AS `strings`,
  `bfcol_8` AS `mixed`,
  `bfcol_9` AS `empty`,
  `bfcol_10` AS `empty_wo_match_nulls`,
  `bfcol_11` AS `ints_wo_match_nulls`,
  `bfcol_12` AS `float_in_ints`
FROM `bfcte_1`