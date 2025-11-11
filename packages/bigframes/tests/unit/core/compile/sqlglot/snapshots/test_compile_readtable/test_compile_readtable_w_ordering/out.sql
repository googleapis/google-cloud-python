WITH `bfcte_0` AS (
  SELECT
    `int64_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
)
SELECT
  `rowindex`,
  `int64_col`
FROM `bfcte_0`
ORDER BY
  `int64_col` ASC NULLS LAST