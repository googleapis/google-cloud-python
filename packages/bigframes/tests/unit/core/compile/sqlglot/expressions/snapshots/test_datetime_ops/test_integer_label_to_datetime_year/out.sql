WITH `bfcte_0` AS (
  SELECT
    `rowindex`,
    `timestamp_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(TIMESTAMP(DATETIME(`rowindex` * 1 + EXTRACT(YEAR FROM `timestamp_col`) + 1, 1, 1, 0, 0, 0)) - INTERVAL 1 DAY AS TIMESTAMP) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `non_fixed_freq_yearly`
FROM `bfcte_1`