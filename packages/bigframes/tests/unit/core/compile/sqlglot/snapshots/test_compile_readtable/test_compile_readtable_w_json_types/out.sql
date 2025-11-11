WITH `bfcte_0` AS (
  SELECT
    `json_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`json_types`
)
SELECT
  `rowindex`,
  `json_col`
FROM `bfcte_0`