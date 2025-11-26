WITH `bfcte_0` AS (
  SELECT
    `date_col`,
    `datetime_col`,
    `time_col`,
    `timestamp_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    FORMAT_DATE('%Y-%m-%d', `date_col`) AS `bfcol_8`,
    FORMAT_DATETIME('%Y-%m-%d', `datetime_col`) AS `bfcol_9`,
    FORMAT_TIME('%Y-%m-%d', `time_col`) AS `bfcol_10`,
    FORMAT_TIMESTAMP('%Y-%m-%d', `timestamp_col`) AS `bfcol_11`
  FROM `bfcte_0`
)
SELECT
  `bfcol_8` AS `date_col`,
  `bfcol_9` AS `datetime_col`,
  `bfcol_10` AS `time_col`,
  `bfcol_11` AS `timestamp_col`
FROM `bfcte_1`