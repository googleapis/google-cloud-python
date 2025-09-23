WITH `bfcte_0` AS (
  SELECT
    `datetime_col` AS `bfcol_0`,
    `numeric_col` AS `bfcol_1`,
    `float64_col` AS `bfcol_2`,
    `time_col` AS `bfcol_3`,
    `timestamp_col` AS `bfcol_4`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    UNIX_MICROS(CAST(`bfcol_0` AS TIMESTAMP)) AS `bfcol_5`,
    UNIX_MICROS(SAFE_CAST(`bfcol_0` AS TIMESTAMP)) AS `bfcol_6`,
    TIME_DIFF(CAST(`bfcol_3` AS TIME), '00:00:00', MICROSECOND) AS `bfcol_7`,
    TIME_DIFF(SAFE_CAST(`bfcol_3` AS TIME), '00:00:00', MICROSECOND) AS `bfcol_8`,
    UNIX_MICROS(`bfcol_4`) AS `bfcol_9`,
    CAST(TRUNC(`bfcol_1`) AS INT64) AS `bfcol_10`,
    CAST(TRUNC(`bfcol_2`) AS INT64) AS `bfcol_11`,
    SAFE_CAST(TRUNC(`bfcol_2`) AS INT64) AS `bfcol_12`,
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