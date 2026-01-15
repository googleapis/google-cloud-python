WITH `bfcte_0` AS (
  SELECT
    `rowindex`,
    `timestamp_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(TIMESTAMP_MICROS(
      CAST(CAST(`rowindex` AS BIGNUMERIC) * 86400000000 + CAST(UNIX_MICROS(CAST(`timestamp_col` AS TIMESTAMP)) AS BIGNUMERIC) AS INT64)
    ) AS TIMESTAMP) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `fixed_freq`
FROM `bfcte_1`