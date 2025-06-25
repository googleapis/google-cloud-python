WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`,
    `rowindex` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bfcol_1` AS `bfcol_4`,
    `bfcol_0` + 1 AS `bfcol_5`
  FROM `bfcte_0`
)
SELECT
  `bfcol_4` AS `rowindex`,
  `bfcol_5` AS `int64_col`
FROM `bfcte_1`