WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_0`,
    `json_col` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`json_types`
), `bfcte_1` AS (
  SELECT
    *,
    JSON_SET(`bfcol_1`, '$.a', 100) AS `bfcol_4`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    JSON_SET(`bfcol_4`, '$.b', 'hi') AS `bfcol_7`
  FROM `bfcte_1`
)
SELECT
  `bfcol_0` AS `rowindex`,
  `bfcol_7` AS `json_col`
FROM `bfcte_2`