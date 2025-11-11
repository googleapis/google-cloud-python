WITH `bfcte_1` AS (
  SELECT
    `bool_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_2` AS (
  SELECT
    `rowindex` AS `bfcol_2`,
    `bool_col` AS `bfcol_3`
  FROM `bfcte_1`
), `bfcte_0` AS (
  SELECT
    `bool_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_3` AS (
  SELECT
    `rowindex` AS `bfcol_6`,
    `bool_col` AS `bfcol_7`
  FROM `bfcte_0`
), `bfcte_4` AS (
  SELECT
    *
  FROM `bfcte_2`
  INNER JOIN `bfcte_3`
    ON COALESCE(CAST(`bfcol_3` AS STRING), '0') = COALESCE(CAST(`bfcol_7` AS STRING), '0')
    AND COALESCE(CAST(`bfcol_3` AS STRING), '1') = COALESCE(CAST(`bfcol_7` AS STRING), '1')
)
SELECT
  `bfcol_2` AS `rowindex_x`,
  `bfcol_3` AS `bool_col`,
  `bfcol_6` AS `rowindex_y`
FROM `bfcte_4`