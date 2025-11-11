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
)
SELECT
  `rowindex`,
  `bool_col`,
  `bytes_col`,
  `date_col`,
  `datetime_col`,
  `geography_col`,
  `int64_col`,
  `int64_too`,
  `numeric_col`,
  `float64_col`,
  `rowindex` AS `rowindex_1`,
  `rowindex_2`,
  `string_col`,
  `time_col`,
  `timestamp_col`,
  `duration_col`
FROM `bfcte_0`