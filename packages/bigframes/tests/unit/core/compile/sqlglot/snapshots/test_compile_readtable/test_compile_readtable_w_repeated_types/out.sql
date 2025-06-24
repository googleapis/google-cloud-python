WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_0`,
    `int_list_col` AS `bfcol_1`,
    `bool_list_col` AS `bfcol_2`,
    `float_list_col` AS `bfcol_3`,
    `date_list_col` AS `bfcol_4`,
    `date_time_list_col` AS `bfcol_5`,
    `numeric_list_col` AS `bfcol_6`,
    `string_list_col` AS `bfcol_7`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`
)
SELECT
  `bfcol_0` AS `rowindex`,
  `bfcol_0` AS `rowindex_1`,
  `bfcol_1` AS `int_list_col`,
  `bfcol_2` AS `bool_list_col`,
  `bfcol_3` AS `float_list_col`,
  `bfcol_4` AS `date_list_col`,
  `bfcol_5` AS `date_time_list_col`,
  `bfcol_6` AS `numeric_list_col`,
  `bfcol_7` AS `string_list_col`
FROM `bfcte_0`