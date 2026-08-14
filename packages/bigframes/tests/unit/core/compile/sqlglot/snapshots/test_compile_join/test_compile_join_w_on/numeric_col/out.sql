WITH `bfcte_0` AS (
  SELECT
    `numeric_col` AS `bfcol_0`,
    `rowindex` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
), `bfcte_1` AS (
  SELECT
    `bfcol_1` AS `bfcol_2`,
    `bfcol_0` AS `bfcol_3`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    `bfcol_1` AS `bfcol_4`,
    `bfcol_0` AS `bfcol_5`
  FROM `bfcte_0`
)
SELECT
  `bfcol_4` AS `rowindex_x`,
  `bfcol_5` AS `numeric_col`,
  `bfcol_2` AS `rowindex_y`
FROM `bfcte_2`
INNER JOIN `bfcte_1`
  ON COALESCE(`bfcol_5`, CAST(0 AS NUMERIC)) = COALESCE(`bfcol_3`, CAST(0 AS NUMERIC))
  AND COALESCE(`bfcol_5`, CAST(1 AS NUMERIC)) = COALESCE(`bfcol_3`, CAST(1 AS NUMERIC))