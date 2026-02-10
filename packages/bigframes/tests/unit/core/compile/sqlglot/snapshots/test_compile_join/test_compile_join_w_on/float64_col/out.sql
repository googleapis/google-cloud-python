WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_2`,
    `float64_col` AS `bfcol_3`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    `rowindex` AS `bfcol_6`,
    `float64_col` AS `bfcol_7`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_2` AS (
  SELECT
    *
  FROM `bfcte_0`
  INNER JOIN `bfcte_1`
    ON IF(IS_NAN(`bfcol_3`), 2, COALESCE(`bfcol_3`, 0)) = IF(IS_NAN(`bfcol_7`), 2, COALESCE(`bfcol_7`, 0))
    AND IF(IS_NAN(`bfcol_3`), 3, COALESCE(`bfcol_3`, 1)) = IF(IS_NAN(`bfcol_7`), 3, COALESCE(`bfcol_7`, 1))
)
SELECT
  `bfcol_2` AS `rowindex_x`,
  `bfcol_3` AS `float64_col`,
  `bfcol_6` AS `rowindex_y`
FROM `bfcte_2`