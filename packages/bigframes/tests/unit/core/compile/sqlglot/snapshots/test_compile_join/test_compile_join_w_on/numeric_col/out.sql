WITH `bfcte_1` AS (
  SELECT
    `numeric_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_2` AS (
  SELECT
    `rowindex` AS `bfcol_2`,
    `numeric_col` AS `bfcol_3`
  FROM `bfcte_1`
), `bfcte_0` AS (
  SELECT
    `numeric_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_3` AS (
  SELECT
    `rowindex` AS `bfcol_6`,
    `numeric_col` AS `bfcol_7`
  FROM `bfcte_0`
), `bfcte_4` AS (
  SELECT
    *
  FROM `bfcte_2`
  INNER JOIN `bfcte_3`
    ON COALESCE(`bfcol_3`, CAST(0 AS NUMERIC)) = COALESCE(`bfcol_7`, CAST(0 AS NUMERIC))
    AND COALESCE(`bfcol_3`, CAST(1 AS NUMERIC)) = COALESCE(`bfcol_7`, CAST(1 AS NUMERIC))
)
SELECT
  `bfcol_2` AS `rowindex_x`,
  `bfcol_3` AS `numeric_col`,
  `bfcol_6` AS `rowindex_y`
FROM `bfcte_4`