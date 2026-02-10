WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_2`,
    `int64_col` AS `bfcol_3`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    `rowindex` AS `bfcol_6`,
    `int64_col` AS `bfcol_7`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_2` AS (
  SELECT
    *
  FROM `bfcte_0`
  INNER JOIN `bfcte_1`
    ON COALESCE(`bfcol_3`, 0) = COALESCE(`bfcol_7`, 0)
    AND COALESCE(`bfcol_3`, 1) = COALESCE(`bfcol_7`, 1)
)
SELECT
  `bfcol_2` AS `rowindex_x`,
  `bfcol_3` AS `int64_col`,
  `bfcol_6` AS `rowindex_y`
FROM `bfcte_2`