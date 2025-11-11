WITH `bfcte_0` AS (
  SELECT
    `int64_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `rowindex` AS `bfcol_5`,
    `rowindex` AS `bfcol_6`,
    `int64_col` AS `bfcol_7`,
    `rowindex` >= 1 AS `bfcol_8`
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