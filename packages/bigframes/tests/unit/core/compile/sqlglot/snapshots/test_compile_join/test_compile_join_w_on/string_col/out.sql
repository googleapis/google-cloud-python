WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_0`,
    `string_col` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    `rowindex` AS `bfcol_4`,
    `string_col` AS `bfcol_5`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_2` AS (
  SELECT
    *
  FROM `bfcte_0`
  INNER JOIN `bfcte_1`
    ON COALESCE(CAST(`bfcol_1` AS STRING), '0') = COALESCE(CAST(`bfcol_5` AS STRING), '0')
    AND COALESCE(CAST(`bfcol_1` AS STRING), '1') = COALESCE(CAST(`bfcol_5` AS STRING), '1')
)
SELECT
  `bfcol_0` AS `rowindex_x`,
  `bfcol_1` AS `string_col`,
  `bfcol_4` AS `rowindex_y`
FROM `bfcte_2`