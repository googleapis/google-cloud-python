WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_0`,
    `json_col` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`json_types`
)
SELECT
  `bfcol_0` AS `rowindex`,
  `bfcol_1` AS `json_col`
FROM `bfcte_0`