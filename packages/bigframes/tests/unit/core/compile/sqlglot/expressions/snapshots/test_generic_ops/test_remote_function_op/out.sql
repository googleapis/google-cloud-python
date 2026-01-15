WITH `bfcte_0` AS (
  SELECT
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `my_project`.`my_dataset`.`my_routine`(`int64_col`) AS `bfcol_1`,
    IF(
      `int64_col` IS NULL,
      `int64_col`,
      `my_project`.`my_dataset`.`my_routine`(`int64_col`)
    ) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `apply_on_null_true`,
  `bfcol_2` AS `apply_on_null_false`
FROM `bfcte_1`