WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    PERCENTILE_CONT(`int64_col`, 0.5) OVER () AS `bfcol_4`,
    PERCENTILE_CONT(CAST(`bool_col` AS INT64), 0.5) OVER () AS `bfcol_5`,
    CAST(FLOOR(PERCENTILE_CONT(`int64_col`, 0.5) OVER ()) AS INT64) AS `bfcol_6`
  FROM `bfcte_0`
)
SELECT
  `bfcol_4` AS `int64`,
  `bfcol_5` AS `bool`,
  `bfcol_6` AS `int64_w_floor`
FROM `bfcte_1`