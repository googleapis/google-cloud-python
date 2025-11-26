WITH `bfcte_0` AS (
  SELECT
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `int64_col` - LAG(`int64_col`, 1) OVER (ORDER BY `int64_col` ASC NULLS LAST) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `diff_int`
FROM `bfcte_1`