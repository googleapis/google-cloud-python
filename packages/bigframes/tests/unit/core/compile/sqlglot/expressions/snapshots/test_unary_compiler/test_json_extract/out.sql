WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_0`,
    `json_col` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`json_types`
), `bfcte_1` AS (
  SELECT
    *,
    JSON_EXTRACT(`bfcol_1`, '$') AS `bfcol_4`
  FROM `bfcte_0`
)
SELECT
  `bfcol_0` AS `rowindex`,
  `bfcol_4` AS `json_col`
FROM `bfcte_1`