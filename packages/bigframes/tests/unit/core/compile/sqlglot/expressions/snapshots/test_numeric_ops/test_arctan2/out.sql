WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `float64_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    ATAN2(`int64_col`, `float64_col`) AS `bfcol_6`,
    ATAN2(CAST(`bool_col` AS INT64), `float64_col`) AS `bfcol_7`
  FROM `bfcte_0`
)
SELECT
  `bfcol_6` AS `int64_col`,
  `bfcol_7` AS `bool_col`
FROM `bfcte_1`