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
    `bfcol_1` AS `bfcol_5`
  FROM `bfcte_0`
)
SELECT
  `bfcol_0` AS `rowindex`,
  `bfcol_1` AS `int64_col`,
  `bfcol_2` AS `string_col`,
  `bfcol_3` AS `float64_col`,
  `bfcol_4` AS `bool_col`
FROM `bfcte_1`
ORDER BY
  `bfcol_5` ASC NULLS LAST
LIMIT 10