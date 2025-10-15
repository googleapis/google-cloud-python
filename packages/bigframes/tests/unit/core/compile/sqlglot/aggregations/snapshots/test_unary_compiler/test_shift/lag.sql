WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    LAG(`bfcol_0`, 1) OVER (ORDER BY `bfcol_0` ASC) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `lag`
FROM `bfcte_1`