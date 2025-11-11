WITH `bfcte_0` AS (
  SELECT
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    PERCENTILE_CONT(`int64_col`, 0.5) OVER () AS `bfcol_1`,
    CAST(FLOOR(PERCENTILE_CONT(`int64_col`, 0.5) OVER ()) AS INT64) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `quantile`,
  `bfcol_2` AS `quantile_floor`
FROM `bfcte_1`