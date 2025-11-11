WITH `bfcte_0` AS (
  SELECT
    `float64_col`,
    `int64_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `rowindex` AS `bfcol_6`,
    `int64_col` AS `bfcol_7`,
    `float64_col` AS `bfcol_8`,
    CAST(ROUND(`int64_col`, 0) AS INT64) AS `bfcol_9`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_6` AS `bfcol_14`,
    `bfcol_7` AS `bfcol_15`,
    `bfcol_8` AS `bfcol_16`,
    `bfcol_9` AS `bfcol_17`,
    CAST(ROUND(`bfcol_7`, 1) AS INT64) AS `bfcol_18`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *,
    `bfcol_14` AS `bfcol_24`,
    `bfcol_15` AS `bfcol_25`,
    `bfcol_16` AS `bfcol_26`,
    `bfcol_17` AS `bfcol_27`,
    `bfcol_18` AS `bfcol_28`,
    CAST(ROUND(`bfcol_15`, -1) AS INT64) AS `bfcol_29`
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
    ROUND(`bfcol_26`, 0) AS `bfcol_42`
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
    ROUND(`bfcol_38`, 1) AS `bfcol_57`
  FROM `bfcte_4`
), `bfcte_6` AS (
  SELECT
    *,
    `bfcol_50` AS `bfcol_66`,
    `bfcol_51` AS `bfcol_67`,
    `bfcol_52` AS `bfcol_68`,
    `bfcol_53` AS `bfcol_69`,
    `bfcol_54` AS `bfcol_70`,
    `bfcol_55` AS `bfcol_71`,
    `bfcol_56` AS `bfcol_72`,
    `bfcol_57` AS `bfcol_73`,
    ROUND(`bfcol_52`, -1) AS `bfcol_74`
  FROM `bfcte_5`
)
SELECT
  `bfcol_66` AS `rowindex`,
  `bfcol_67` AS `int64_col`,
  `bfcol_68` AS `float64_col`,
  `bfcol_69` AS `int_round_0`,
  `bfcol_70` AS `int_round_1`,
  `bfcol_71` AS `int_round_m1`,
  `bfcol_72` AS `float_round_0`,
  `bfcol_73` AS `float_round_1`,
  `bfcol_74` AS `float_round_m1`
FROM `bfcte_6`