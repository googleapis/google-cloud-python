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
    `timestamp_col` AS `bfcol_13`,
    `duration_col` AS `bfcol_14`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    ROW_NUMBER() OVER () AS `bfcol_32`
  FROM `bfcte_0`
)
SELECT
  `bfcol_32` AS `row_number`
FROM `bfcte_1`