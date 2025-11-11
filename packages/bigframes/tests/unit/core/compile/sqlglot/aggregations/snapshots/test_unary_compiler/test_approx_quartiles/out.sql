WITH `bfcte_0` AS (
  SELECT
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    APPROX_QUANTILES(`int64_col`, 4)[OFFSET(1)] AS `bfcol_1`,
    APPROX_QUANTILES(`int64_col`, 4)[OFFSET(2)] AS `bfcol_2`,
    APPROX_QUANTILES(`int64_col`, 4)[OFFSET(3)] AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `q1`,
  `bfcol_2` AS `q2`,
  `bfcol_3` AS `q3`
FROM `bfcte_1`