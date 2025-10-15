WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bfcol_0` <> LAG(`bfcol_0`, 1) OVER (ORDER BY `bfcol_0` DESC) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `diff_bool`
FROM `bfcte_1`