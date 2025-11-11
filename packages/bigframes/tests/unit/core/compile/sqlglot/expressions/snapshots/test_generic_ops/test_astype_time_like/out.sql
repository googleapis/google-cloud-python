WITH `bfcte_0` AS (
  SELECT
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(TIMESTAMP_MICROS(`int64_col`) AS DATETIME) AS `bfcol_1`,
    CAST(TIMESTAMP_MICROS(`int64_col`) AS TIME) AS `bfcol_2`,
    CAST(TIMESTAMP_MICROS(`int64_col`) AS TIMESTAMP) AS `bfcol_3`,
    SAFE_CAST(TIMESTAMP_MICROS(`int64_col`) AS TIME) AS `bfcol_4`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `int64_to_datetime`,
  `bfcol_2` AS `int64_to_time`,
  `bfcol_3` AS `int64_to_timestamp`,
  `bfcol_4` AS `int64_to_time_safe`
FROM `bfcte_1`