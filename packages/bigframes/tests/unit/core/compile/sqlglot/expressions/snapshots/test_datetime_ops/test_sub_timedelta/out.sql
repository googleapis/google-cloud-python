WITH `bfcte_0` AS (
  SELECT
    `date_col` AS `bfcol_0`,
    `rowindex` AS `bfcol_1`,
    `timestamp_col` AS `bfcol_2`,
    `duration_col` AS `bfcol_3`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bfcol_1` AS `bfcol_8`,
    `bfcol_2` AS `bfcol_9`,
    `bfcol_0` AS `bfcol_10`,
    `bfcol_3` AS `bfcol_11`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_8` AS `bfcol_16`,
    `bfcol_9` AS `bfcol_17`,
    `bfcol_11` AS `bfcol_18`,
    `bfcol_10` AS `bfcol_19`,
    TIMESTAMP_SUB(CAST(`bfcol_10` AS DATETIME), INTERVAL `bfcol_11` MICROSECOND) AS `bfcol_20`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *,
    `bfcol_16` AS `bfcol_26`,
    `bfcol_17` AS `bfcol_27`,
    `bfcol_18` AS `bfcol_28`,
    `bfcol_19` AS `bfcol_29`,
    `bfcol_20` AS `bfcol_30`,
    TIMESTAMP_SUB(`bfcol_17`, INTERVAL `bfcol_18` MICROSECOND) AS `bfcol_31`
  FROM `bfcte_2`
), `bfcte_4` AS (
  SELECT
    *,
    `bfcol_26` AS `bfcol_38`,
    `bfcol_27` AS `bfcol_39`,
    `bfcol_28` AS `bfcol_40`,
    `bfcol_29` AS `bfcol_41`,
    `bfcol_30` AS `bfcol_42`,
    `bfcol_31` AS `bfcol_43`,
    TIMESTAMP_DIFF(CAST(`bfcol_29` AS DATETIME), CAST(`bfcol_29` AS DATETIME), MICROSECOND) AS `bfcol_44`
  FROM `bfcte_3`
), `bfcte_5` AS (
  SELECT
    *,
    `bfcol_38` AS `bfcol_52`,
    `bfcol_39` AS `bfcol_53`,
    `bfcol_40` AS `bfcol_54`,
    `bfcol_41` AS `bfcol_55`,
    `bfcol_42` AS `bfcol_56`,
    `bfcol_43` AS `bfcol_57`,
    `bfcol_44` AS `bfcol_58`,
    TIMESTAMP_DIFF(`bfcol_39`, `bfcol_39`, MICROSECOND) AS `bfcol_59`
  FROM `bfcte_4`
), `bfcte_6` AS (
  SELECT
    *,
    `bfcol_52` AS `bfcol_68`,
    `bfcol_53` AS `bfcol_69`,
    `bfcol_54` AS `bfcol_70`,
    `bfcol_55` AS `bfcol_71`,
    `bfcol_56` AS `bfcol_72`,
    `bfcol_57` AS `bfcol_73`,
    `bfcol_58` AS `bfcol_74`,
    `bfcol_59` AS `bfcol_75`,
    `bfcol_54` - `bfcol_54` AS `bfcol_76`
  FROM `bfcte_5`
)
SELECT
  `bfcol_68` AS `rowindex`,
  `bfcol_69` AS `timestamp_col`,
  `bfcol_70` AS `duration_col`,
  `bfcol_71` AS `date_col`,
  `bfcol_72` AS `date_sub_timedelta`,
  `bfcol_73` AS `timestamp_sub_timedelta`,
  `bfcol_74` AS `timestamp_sub_date`,
  `bfcol_75` AS `date_sub_timestamp`,
  `bfcol_76` AS `timedelta_sub_timedelta`
FROM `bfcte_6`