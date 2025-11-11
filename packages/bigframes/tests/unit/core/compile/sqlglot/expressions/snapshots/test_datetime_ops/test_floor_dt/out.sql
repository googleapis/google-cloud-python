WITH `bfcte_0` AS (
  SELECT
    `datetime_col`,
    `timestamp_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    TIMESTAMP_TRUNC(`timestamp_col`, MICROSECOND) AS `bfcol_2`,
    TIMESTAMP_TRUNC(`timestamp_col`, MILLISECOND) AS `bfcol_3`,
    TIMESTAMP_TRUNC(`timestamp_col`, SECOND) AS `bfcol_4`,
    TIMESTAMP_TRUNC(`timestamp_col`, MINUTE) AS `bfcol_5`,
    TIMESTAMP_TRUNC(`timestamp_col`, HOUR) AS `bfcol_6`,
    TIMESTAMP_TRUNC(`timestamp_col`, DAY) AS `bfcol_7`,
    TIMESTAMP_TRUNC(`timestamp_col`, WEEK(MONDAY)) AS `bfcol_8`,
    TIMESTAMP_TRUNC(`timestamp_col`, MONTH) AS `bfcol_9`,
    TIMESTAMP_TRUNC(`timestamp_col`, QUARTER) AS `bfcol_10`,
    TIMESTAMP_TRUNC(`timestamp_col`, YEAR) AS `bfcol_11`,
    TIMESTAMP_TRUNC(`datetime_col`, MICROSECOND) AS `bfcol_12`,
    TIMESTAMP_TRUNC(`datetime_col`, MICROSECOND) AS `bfcol_13`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `timestamp_col_us`,
  `bfcol_3` AS `timestamp_col_ms`,
  `bfcol_4` AS `timestamp_col_s`,
  `bfcol_5` AS `timestamp_col_min`,
  `bfcol_6` AS `timestamp_col_h`,
  `bfcol_7` AS `timestamp_col_D`,
  `bfcol_8` AS `timestamp_col_W`,
  `bfcol_9` AS `timestamp_col_M`,
  `bfcol_10` AS `timestamp_col_Q`,
  `bfcol_11` AS `timestamp_col_Y`,
  `bfcol_12` AS `datetime_col_q`,
  `bfcol_13` AS `datetime_col_us`
FROM `bfcte_1`