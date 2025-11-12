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
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` FOR SYSTEM_TIME AS OF '2025-11-09T03:04:05.678901+00:00'
)
SELECT
  `bool_col`,
  `bytes_col`,
  `date_col`,
  `datetime_col`,
  `geography_col`,
  `int64_col`,
  `int64_too`,
  `numeric_col`,
  `float64_col`,
  `rowindex`,
  `rowindex_2`,
  `string_col`,
  `time_col`,
  `timestamp_col`,
  `duration_col`
FROM `bfcte_0`