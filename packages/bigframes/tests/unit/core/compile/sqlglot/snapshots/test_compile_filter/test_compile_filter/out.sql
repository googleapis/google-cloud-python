WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`,
    `rowindex` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bfcol_1` AS `bfcol_5`,
    `bfcol_1` AS `bfcol_6`,
    `bfcol_0` AS `bfcol_7`,
    `bfcol_1` >= 1 AS `bfcol_8`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *
  FROM `bfcte_1`
  WHERE
    `bfcol_8`
)
SELECT
  `bfcol_5` AS `rowindex`,
  `bfcol_6` AS `rowindex_1`,
  `bfcol_7` AS `int64_col`
FROM `bfcte_2`