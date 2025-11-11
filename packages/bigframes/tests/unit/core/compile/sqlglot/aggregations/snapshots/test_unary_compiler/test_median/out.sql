WITH `bfcte_0` AS (
  SELECT
    `date_col`,
    `int64_col`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    APPROX_QUANTILES(`int64_col`, 2)[OFFSET(1)] AS `bfcol_3`,
    APPROX_QUANTILES(`date_col`, 2)[OFFSET(1)] AS `bfcol_4`,
    APPROX_QUANTILES(`string_col`, 2)[OFFSET(1)] AS `bfcol_5`
  FROM `bfcte_0`
)
SELECT
  `bfcol_3` AS `int64_col`,
  `bfcol_4` AS `date_col`,
  `bfcol_5` AS `string_col`
FROM `bfcte_1`