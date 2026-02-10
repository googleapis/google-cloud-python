WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_2`,
    `numeric_col` AS `bfcol_3`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    `rowindex` AS `bfcol_6`,
    `numeric_col` AS `bfcol_7`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_2` AS (
  SELECT
    *
  FROM `bfcte_0`
  INNER JOIN `bfcte_1`
    ON COALESCE(`bfcol_3`, CAST(0 AS NUMERIC)) = COALESCE(`bfcol_7`, CAST(0 AS NUMERIC))
    AND COALESCE(`bfcol_3`, CAST(1 AS NUMERIC)) = COALESCE(`bfcol_7`, CAST(1 AS NUMERIC))
)
SELECT
  `bfcol_2` AS `rowindex_x`,
  `bfcol_3` AS `numeric_col`,
  `bfcol_6` AS `rowindex_y`
FROM `bfcte_2`