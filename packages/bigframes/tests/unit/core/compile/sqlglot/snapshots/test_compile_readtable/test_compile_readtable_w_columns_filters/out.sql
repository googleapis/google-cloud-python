WITH `bfcte_0` AS (
  SELECT
    *
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
  WHERE
    `rowindex` > 0 AND `string_col` IN ('Hello, World!')
)
SELECT
  *
FROM `bfcte_0`