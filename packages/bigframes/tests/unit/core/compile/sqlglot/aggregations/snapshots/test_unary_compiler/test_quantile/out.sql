WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    PERCENTILE_CONT(`bfcol_0`, 0.5) OVER () AS `bfcol_1`,
    CAST(FLOOR(PERCENTILE_CONT(`bfcol_0`, 0.5) OVER ()) AS INT64) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `quantile`,
  `bfcol_2` AS `quantile_floor`
FROM `bfcte_1`