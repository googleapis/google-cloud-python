WITH `bfcte_0` AS (
  SELECT
    `int64_col`,
    `rowindex`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
  WHERE
    `rowindex` > 0 AND `string_col` IN ('Hello, World!')
)
SELECT
  `rowindex`,
  `int64_col`,
  `string_col`
FROM `bfcte_0`