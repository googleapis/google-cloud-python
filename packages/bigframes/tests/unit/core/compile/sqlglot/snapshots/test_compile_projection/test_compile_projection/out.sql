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
    `bfcol_1` + 1 AS `bfcol_9`
  FROM `bfcte_0`
)
SELECT
  `bfcol_5` AS `rowindex`,
  `bfcol_9` AS `int64_col`,
  `bfcol_6` AS `string_col`,
  `bfcol_7` AS `float64_col`,
  `bfcol_8` AS `bool_col`
FROM `bfcte_1`