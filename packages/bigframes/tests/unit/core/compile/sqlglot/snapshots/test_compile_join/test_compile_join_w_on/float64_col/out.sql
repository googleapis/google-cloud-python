WITH `bfcte_1` AS (
  SELECT
    `float64_col` AS `bfcol_0`,
    `rowindex` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_2` AS (
  SELECT
    `bfcol_1` AS `bfcol_2`,
    `bfcol_0` AS `bfcol_3`
  FROM `bfcte_1`
), `bfcte_0` AS (
  SELECT
    `float64_col` AS `bfcol_4`,
    `rowindex` AS `bfcol_5`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_3` AS (
  SELECT
    `bfcol_5` AS `bfcol_6`,
    `bfcol_4` AS `bfcol_7`
  FROM `bfcte_0`
), `bfcte_4` AS (
  SELECT
    *
  FROM `bfcte_2`
  INNER JOIN `bfcte_3`
    ON   IF(IS_NAN(`bfcol_3`), 2, COALESCE(`bfcol_3`, 0)) = IF(IS_NAN(`bfcol_7`), 2, COALESCE(`bfcol_7`, 0))
      AND IF(IS_NAN(`bfcol_3`), 3, COALESCE(`bfcol_3`, 1)) = IF(IS_NAN(`bfcol_7`), 3, COALESCE(`bfcol_7`, 1))
)
SELECT
  `bfcol_2` AS `rowindex_x`,
  `bfcol_3` AS `float64_col`,
  `bfcol_6` AS `rowindex_y`
FROM `bfcte_4`