WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_0`,
    `int64_col` AS `bfcol_1`,
    `string_col` AS `bfcol_2`,
    `float64_col` AS `bfcol_3`,
    `bool_col` AS `bfcol_4`
  FROM `test-project`.`test_dataset`.`test_table`
), `bfcte_1` AS (
  SELECT
    *,
    `bfcol_0` AS `bfcol_5`,
    `bfcol_2` AS `bfcol_6`,
    `bfcol_3` AS `bfcol_7`,
    `bfcol_4` AS `bfcol_8`,
    `bfcol_1` + `bfcol_1` AS `bfcol_9`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    `bfcol_5` AS `bfcol_10`,
    `bfcol_9` AS `bfcol_11`,
    `bfcol_6` AS `bfcol_12`,
    `bfcol_7` AS `bfcol_13`,
    `bfcol_8` AS `bfcol_14`
  FROM `bfcte_1`
)
SELECT
  `bfcol_10` AS `rowindex`,
  `bfcol_11` AS `int64_col`,
  `bfcol_12` AS `string_col`,
  `bfcol_13` AS `float64_col`,
  `bfcol_14` AS `bool_col`
FROM `bfcte_2`