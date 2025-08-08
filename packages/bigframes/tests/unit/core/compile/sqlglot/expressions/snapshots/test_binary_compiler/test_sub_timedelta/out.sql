WITH `bfcte_0` AS (
  SELECT
    `date_col` AS `bfcol_0`,
    `rowindex` AS `bfcol_1`,
    `timestamp_col` AS `bfcol_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bfcol_1` AS `bfcol_6`,
    `bfcol_2` AS `bfcol_7`,
    `bfcol_0` AS `bfcol_8`,
    TIMESTAMP_SUB(CAST(`bfcol_0` AS DATETIME), INTERVAL 86400000000 MICROSECOND) AS `bfcol_9`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_6` AS `bfcol_14`,
    `bfcol_7` AS `bfcol_15`,
    `bfcol_8` AS `bfcol_16`,
    `bfcol_9` AS `bfcol_17`,
    TIMESTAMP_SUB(`bfcol_7`, INTERVAL 86400000000 MICROSECOND) AS `bfcol_18`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *,
    `bfcol_14` AS `bfcol_24`,
    `bfcol_15` AS `bfcol_25`,
    `bfcol_16` AS `bfcol_26`,
    `bfcol_17` AS `bfcol_27`,
    `bfcol_18` AS `bfcol_28`,
    TIMESTAMP_DIFF(CAST(`bfcol_16` AS DATETIME), CAST(`bfcol_16` AS DATETIME), MICROSECOND) AS `bfcol_29`
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
    TIMESTAMP_DIFF(`bfcol_25`, `bfcol_25`, MICROSECOND) AS `bfcol_42`
  FROM `bfcte_3`
), `bfcte_5` AS (
  SELECT
    *,
    0 AS `bfcol_50`
  FROM `bfcte_4`
)
SELECT
  `bfcol_36` AS `rowindex`,
  `bfcol_37` AS `timestamp_col`,
  `bfcol_38` AS `date_col`,
  `bfcol_39` AS `date_sub_timedelta`,
  `bfcol_40` AS `timestamp_sub_timedelta`,
  `bfcol_41` AS `timestamp_sub_date`,
  `bfcol_42` AS `date_sub_timestamp`,
  `bfcol_50` AS `timedelta_sub_timedelta`
FROM `bfcte_5`