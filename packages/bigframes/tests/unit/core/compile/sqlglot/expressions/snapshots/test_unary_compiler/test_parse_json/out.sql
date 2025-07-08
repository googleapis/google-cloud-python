WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_0`,
    `string_col` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    JSON_VALUE(`bfcol_1`, '$') AS `bfcol_4`
  FROM `bfcte_0`
)
SELECT
  `bfcol_0` AS `rowindex`,
  `bfcol_4` AS `string_col`
FROM `bfcte_1`