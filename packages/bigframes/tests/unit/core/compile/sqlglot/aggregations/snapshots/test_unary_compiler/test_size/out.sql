WITH `bfcte_0` AS (
  SELECT
    `string_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    COUNT(1) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `string_col_agg`
FROM `bfcte_1`