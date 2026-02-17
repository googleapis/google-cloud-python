WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_2`,
    `bool_col` AS `bfcol_3`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
), `bfcte_1` AS (
  SELECT
    `rowindex` AS `bfcol_6`,
    `bool_col` AS `bfcol_7`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
), `bfcte_2` AS (
  SELECT
    *
  FROM `bfcte_0`
  INNER JOIN `bfcte_1`
    ON COALESCE(CAST(`bfcol_3` AS STRING), '0') = COALESCE(CAST(`bfcol_7` AS STRING), '0')
    AND COALESCE(CAST(`bfcol_3` AS STRING), '1') = COALESCE(CAST(`bfcol_7` AS STRING), '1')
)
SELECT
  `bfcol_2` AS `rowindex_x`,
  `bfcol_3` AS `bool_col`,
  `bfcol_6` AS `rowindex_y`
FROM `bfcte_2`