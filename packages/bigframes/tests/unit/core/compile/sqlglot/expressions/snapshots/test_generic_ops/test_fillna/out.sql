WITH `bfcte_0` AS (
  SELECT
    `float64_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    COALESCE(`int64_col`, `float64_col`) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `int64_col`
FROM `bfcte_1`