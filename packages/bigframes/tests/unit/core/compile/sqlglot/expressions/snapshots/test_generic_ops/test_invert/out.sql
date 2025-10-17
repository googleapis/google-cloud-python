WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `bytes_col` AS `bfcol_1`,
    `int64_col` AS `bfcol_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    ~`bfcol_2` AS `bfcol_6`,
    ~`bfcol_1` AS `bfcol_7`,
    NOT `bfcol_0` AS `bfcol_8`
  FROM `bfcte_0`
)
SELECT
  `bfcol_6` AS `int64_col`,
  `bfcol_7` AS `bytes_col`,
  `bfcol_8` AS `bool_col`
FROM `bfcte_1`