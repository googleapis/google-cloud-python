WITH `bfcte_0` AS (
  SELECT
    `rowindex`,
    `timestamp_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(TIMESTAMP_MICROS(
      CAST(CAST(`rowindex` AS BIGNUMERIC) * 604800000000 + CAST(UNIX_MICROS(
        TIMESTAMP_TRUNC(CAST(`timestamp_col` AS TIMESTAMP), WEEK(MONDAY)) + INTERVAL 6 DAY
      ) AS BIGNUMERIC) AS INT64)
    ) AS TIMESTAMP) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `non_fixed_freq_weekly`
FROM `bfcte_1`