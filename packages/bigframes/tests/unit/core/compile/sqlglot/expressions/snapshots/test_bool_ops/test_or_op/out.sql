WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `int64_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `rowindex` AS `bfcol_6`,
    `bool_col` AS `bfcol_7`,
    `int64_col` AS `bfcol_8`,
    `int64_col` | `int64_col` AS `bfcol_9`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_6` AS `bfcol_14`,
    `bfcol_7` AS `bfcol_15`,
    `bfcol_8` AS `bfcol_16`,
    `bfcol_9` AS `bfcol_17`,
    `bfcol_7` OR `bfcol_7` AS `bfcol_18`
  FROM `bfcte_1`
)
SELECT
  `bfcol_14` AS `rowindex`,
  `bfcol_15` AS `bool_col`,
  `bfcol_16` AS `int64_col`,
  `bfcol_17` AS `int_and_int`,
  `bfcol_18` AS `bool_and_bool`
FROM `bfcte_2`