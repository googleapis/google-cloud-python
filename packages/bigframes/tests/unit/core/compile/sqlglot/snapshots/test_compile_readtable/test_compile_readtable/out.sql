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
), `bfcte_1` AS (
  SELECT
    `bfcol_9` AS `bfcol_14`,
    `bfcol_0` AS `bfcol_15`,
    `bfcol_1` AS `bfcol_16`,
    `bfcol_2` AS `bfcol_17`,
    `bfcol_3` AS `bfcol_18`,
    `bfcol_4` AS `bfcol_19`,
    `bfcol_5` AS `bfcol_20`,
    `bfcol_6` AS `bfcol_21`,
    `bfcol_7` AS `bfcol_22`,
    `bfcol_8` AS `bfcol_23`,
    `bfcol_9` AS `bfcol_24`,
    `bfcol_10` AS `bfcol_25`,
    `bfcol_11` AS `bfcol_26`,
    `bfcol_12` AS `bfcol_27`,
    `bfcol_13` AS `bfcol_28`
  FROM `bfcte_0`
)
SELECT
  `bfcol_14` AS `rowindex`,
  `bfcol_15` AS `bool_col`,
  `bfcol_16` AS `bytes_col`,
  `bfcol_17` AS `date_col`,
  `bfcol_18` AS `datetime_col`,
  `bfcol_19` AS `geography_col`,
  `bfcol_20` AS `int64_col`,
  `bfcol_21` AS `int64_too`,
  `bfcol_22` AS `numeric_col`,
  `bfcol_23` AS `float64_col`,
  `bfcol_24` AS `rowindex_1`,
  `bfcol_25` AS `rowindex_2`,
  `bfcol_26` AS `string_col`,
  `bfcol_27` AS `time_col`,
  `bfcol_28` AS `timestamp_col`
FROM `bfcte_1`