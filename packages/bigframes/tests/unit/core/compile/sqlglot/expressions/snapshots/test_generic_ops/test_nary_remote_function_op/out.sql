WITH `bfcte_0` AS (
  SELECT
    `float64_col`,
    `int64_col`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `my_project`.`my_dataset`.`my_routine`(`int64_col`, `float64_col`, `string_col`) AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_3` AS `int64_col`
FROM `bfcte_1`