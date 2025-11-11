WITH `bfcte_0` AS (
  SELECT
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    ROW_NUMBER() OVER (ORDER BY `int64_col` ASC NULLS LAST) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `row_number`
FROM `bfcte_1`