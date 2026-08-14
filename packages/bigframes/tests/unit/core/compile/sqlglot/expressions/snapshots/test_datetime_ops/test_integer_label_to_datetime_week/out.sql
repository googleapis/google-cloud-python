SELECT
  CAST(TIMESTAMP_MICROS(
    CAST(CAST(`rowindex` AS BIGNUMERIC) * 604800000000 + CAST(UNIX_MICROS(
      TIMESTAMP_TRUNC(CAST(`timestamp_col` AS TIMESTAMP), WEEK(MONDAY)) + INTERVAL 6 DAY
    ) AS BIGNUMERIC) AS INT64)
  ) AS TIMESTAMP) AS `non_fixed_freq_weekly`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`