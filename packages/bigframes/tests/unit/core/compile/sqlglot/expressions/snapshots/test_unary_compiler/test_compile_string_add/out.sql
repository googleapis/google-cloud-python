WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_0`,
    `string_col` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bfcol_0` AS `bfcol_4`,
    CONCAT(`bfcol_1`, 'a') AS `bfcol_5`
  FROM `bfcte_0`
)
SELECT
  `bfcol_4` AS `rowindex`,
  `bfcol_5` AS `string_col`
FROM `bfcte_1`