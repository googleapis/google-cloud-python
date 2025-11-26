WITH `bfcte_0` AS (
  SELECT
    `bool_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bool_col` <> LAG(`bool_col`, 1) OVER (ORDER BY `bool_col` DESC) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `diff_bool`
FROM `bfcte_1`