WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`,
    `rowindex` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
)
SELECT
  `bfcol_1` AS `rowindex`,
  `bfcol_0` AS `int64_col`
FROM `bfcte_0`
ORDER BY
  `bfcol_1` ASC NULLS LAST
LIMIT 10