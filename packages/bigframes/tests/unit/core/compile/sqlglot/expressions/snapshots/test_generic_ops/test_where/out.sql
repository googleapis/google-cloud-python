WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `float64_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    IF(`bool_col`, `int64_col`, `float64_col`) AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_3` AS `result_col`
FROM `bfcte_1`