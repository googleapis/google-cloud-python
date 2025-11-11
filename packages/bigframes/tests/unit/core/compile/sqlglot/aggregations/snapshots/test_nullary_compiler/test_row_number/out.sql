WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `bytes_col`,
    `date_col`,
    `datetime_col`,
    `duration_col`,
    `float64_col`,
    `geography_col`,
    `int64_col`,
    `int64_too`,
    `numeric_col`,
    `rowindex`,
    `rowindex_2`,
    `string_col`,
    `time_col`,
    `timestamp_col`
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