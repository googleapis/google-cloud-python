SELECT
  CAST(TIMESTAMP_MICROS(
    CAST(CAST(`rowindex` AS BIGNUMERIC) * 86400000000 + CAST(UNIX_MICROS(CAST(`timestamp_col` AS TIMESTAMP)) AS BIGNUMERIC) AS INT64)
  ) AS TIMESTAMP) AS `fixed_freq`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`