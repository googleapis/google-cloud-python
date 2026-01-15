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
    `int64_col` <> `int64_col` AS `bfcol_9`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_6` AS `bfcol_14`,
    `bfcol_7` AS `bfcol_15`,
    `bfcol_8` AS `bfcol_16`,
    `bfcol_9` AS `bfcol_17`,
    `bfcol_7` <> 1 AS `bfcol_18`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *,
    `bfcol_14` AS `bfcol_24`,
    `bfcol_15` AS `bfcol_25`,
    `bfcol_16` AS `bfcol_26`,
    `bfcol_17` AS `bfcol_27`,
    `bfcol_18` AS `bfcol_28`,
    (
      `bfcol_15`
    ) IS NOT NULL AS `bfcol_29`
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
    `bfcol_25` <> CAST(`bfcol_26` AS INT64) AS `bfcol_42`
  FROM `bfcte_3`
), `bfcte_5` AS (
  SELECT
    *,
    `bfcol_36` AS `bfcol_50`,
    `bfcol_37` AS `bfcol_51`,
    `bfcol_38` AS `bfcol_52`,
    `bfcol_39` AS `bfcol_53`,
    `bfcol_40` AS `bfcol_54`,
    `bfcol_41` AS `bfcol_55`,
    `bfcol_42` AS `bfcol_56`,
    CAST(`bfcol_38` AS INT64) <> `bfcol_37` AS `bfcol_57`
  FROM `bfcte_4`
)
SELECT
  `bfcol_50` AS `rowindex`,
  `bfcol_51` AS `int64_col`,
  `bfcol_52` AS `bool_col`,
  `bfcol_53` AS `int_ne_int`,
  `bfcol_54` AS `int_ne_1`,
  `bfcol_55` AS `int_ne_null`,
  `bfcol_56` AS `int_ne_bool`,
  `bfcol_57` AS `bool_ne_int`
FROM `bfcte_5`