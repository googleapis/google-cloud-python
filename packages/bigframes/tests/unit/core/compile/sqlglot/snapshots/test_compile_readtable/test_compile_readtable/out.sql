WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `bytes_col` AS `bfcol_1`,
    `date_col` AS `bfcol_2`,
    `datetime_col` AS `bfcol_3`,
    `geography_col` AS `bfcol_4`,
    `int64_col` AS `bfcol_5`,
    `int64_too` AS `bfcol_6`,
    `numeric_col` AS `bfcol_7`,
    `float64_col` AS `bfcol_8`,
    `rowindex` AS `bfcol_9`,
    `rowindex_2` AS `bfcol_10`,
    `string_col` AS `bfcol_11`,
    `time_col` AS `bfcol_12`,
    `timestamp_col` AS `bfcol_13`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
)
SELECT
  `bfcol_9` AS `rowindex`,
  `bfcol_0` AS `bool_col`,
  `bfcol_1` AS `bytes_col`,
  `bfcol_2` AS `date_col`,
  `bfcol_3` AS `datetime_col`,
  `bfcol_4` AS `geography_col`,
  `bfcol_5` AS `int64_col`,
  `bfcol_6` AS `int64_too`,
  `bfcol_7` AS `numeric_col`,
  `bfcol_8` AS `float64_col`,
  `bfcol_9` AS `rowindex_1`,
  `bfcol_10` AS `rowindex_2`,
  `bfcol_11` AS `string_col`,
  `bfcol_12` AS `time_col`,
  `bfcol_13` AS `timestamp_col`
FROM `bfcte_0`