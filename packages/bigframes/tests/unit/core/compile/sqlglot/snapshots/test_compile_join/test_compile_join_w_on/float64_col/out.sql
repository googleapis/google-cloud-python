WITH `bfcte_0` AS (
  SELECT
    `float64_col` AS `bfcol_0`,
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
  `bfcol_5` AS `float64_col`,
  `bfcol_2` AS `rowindex_y`
FROM `bfcte_2`
INNER JOIN `bfcte_1`
  ON IF(IS_NAN(`bfcol_5`), 2.0, COALESCE(`bfcol_5`, 0.0)) = IF(IS_NAN(`bfcol_3`), 2.0, COALESCE(`bfcol_3`, 0.0))
  AND IF(IS_NAN(`bfcol_5`), 3, COALESCE(`bfcol_5`, 1.0)) = IF(IS_NAN(`bfcol_3`), 3, COALESCE(`bfcol_3`, 1.0))