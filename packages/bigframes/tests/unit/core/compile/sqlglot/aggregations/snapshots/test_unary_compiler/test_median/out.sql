WITH `bfcte_0` AS (
  SELECT
    `date_col` AS `bfcol_0`,
    `int64_col` AS `bfcol_1`,
    `string_col` AS `bfcol_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    APPROX_QUANTILES(`bfcol_1`, 2)[OFFSET(1)] AS `bfcol_3`,
    APPROX_QUANTILES(`bfcol_0`, 2)[OFFSET(1)] AS `bfcol_4`,
    APPROX_QUANTILES(`bfcol_2`, 2)[OFFSET(1)] AS `bfcol_5`
  FROM `bfcte_0`
)
SELECT
  `bfcol_3` AS `int64_col`,
  `bfcol_4` AS `date_col`,
  `bfcol_5` AS `string_col`
FROM `bfcte_1`