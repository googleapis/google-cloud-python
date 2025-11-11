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
    `int64_col` AS `bfcol_7`,
    `bool_col` AS `bfcol_8`,
    `int64_col` >= `int64_col` AS `bfcol_9`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_6` AS `bfcol_14`,
    `bfcol_7` AS `bfcol_15`,
    `bfcol_8` AS `bfcol_16`,
    `bfcol_9` AS `bfcol_17`,
    `bfcol_7` >= 1 AS `bfcol_18`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *,
    `bfcol_14` AS `bfcol_24`,
    `bfcol_15` AS `bfcol_25`,
    `bfcol_16` AS `bfcol_26`,
    `bfcol_17` AS `bfcol_27`,
    `bfcol_18` AS `bfcol_28`,
    `bfcol_15` >= CAST(`bfcol_16` AS INT64) AS `bfcol_29`
  FROM `bfcte_2`
), `bfcte_4` AS (
  SELECT
    *,
    `bfcol_24` AS `bfcol_36`,
    `bfcol_25` AS `bfcol_37`,
    `bfcol_26` AS `bfcol_38`,
    `bfcol_27` AS `bfcol_39`,
    `bfcol_28` AS `bfcol_40`,
    `bfcol_29` AS `bfcol_41`,
    CAST(`bfcol_26` AS INT64) >= `bfcol_25` AS `bfcol_42`
  FROM `bfcte_3`
)
SELECT
  `bfcol_36` AS `rowindex`,
  `bfcol_37` AS `int64_col`,
  `bfcol_38` AS `bool_col`,
  `bfcol_39` AS `int_ge_int`,
  `bfcol_40` AS `int_ge_1`,
  `bfcol_41` AS `int_ge_bool`,
  `bfcol_42` AS `bool_ge_int`
FROM `bfcte_4`