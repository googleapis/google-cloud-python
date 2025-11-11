WITH `bfcte_0` AS (
  SELECT
    `datetime_col`,
    `float64_col`,
    `numeric_col`,
    `time_col`,
    `timestamp_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    UNIX_MICROS(CAST(`datetime_col` AS TIMESTAMP)) AS `bfcol_5`,
    UNIX_MICROS(SAFE_CAST(`datetime_col` AS TIMESTAMP)) AS `bfcol_6`,
    TIME_DIFF(CAST(`time_col` AS TIME), '00:00:00', MICROSECOND) AS `bfcol_7`,
    TIME_DIFF(SAFE_CAST(`time_col` AS TIME), '00:00:00', MICROSECOND) AS `bfcol_8`,
    UNIX_MICROS(`timestamp_col`) AS `bfcol_9`,
    CAST(TRUNC(`numeric_col`) AS INT64) AS `bfcol_10`,
    CAST(TRUNC(`float64_col`) AS INT64) AS `bfcol_11`,
    SAFE_CAST(TRUNC(`float64_col`) AS INT64) AS `bfcol_12`,
    CAST('100' AS INT64) AS `bfcol_13`
  FROM `bfcte_0`
)
SELECT
  `bfcol_5` AS `datetime_col`,
  `bfcol_6` AS `datetime_w_safe`,
  `bfcol_7` AS `time_col`,
  `bfcol_8` AS `time_w_safe`,
  `bfcol_9` AS `timestamp_col`,
  `bfcol_10` AS `numeric_col`,
  `bfcol_11` AS `float64_col`,
  `bfcol_12` AS `float64_w_safe`,
  `bfcol_13` AS `str_const`
FROM `bfcte_1`