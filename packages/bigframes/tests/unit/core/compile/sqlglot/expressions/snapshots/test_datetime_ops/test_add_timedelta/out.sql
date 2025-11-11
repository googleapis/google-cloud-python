WITH `bfcte_0` AS (
  SELECT
    `date_col`,
    `rowindex`,
    `timestamp_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `rowindex` AS `bfcol_6`,
    `timestamp_col` AS `bfcol_7`,
    `date_col` AS `bfcol_8`,
    TIMESTAMP_ADD(CAST(`date_col` AS DATETIME), INTERVAL 86400000000 MICROSECOND) AS `bfcol_9`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_6` AS `bfcol_14`,
    `bfcol_7` AS `bfcol_15`,
    `bfcol_8` AS `bfcol_16`,
    `bfcol_9` AS `bfcol_17`,
    TIMESTAMP_ADD(`bfcol_7`, INTERVAL 86400000000 MICROSECOND) AS `bfcol_18`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *,
    `bfcol_14` AS `bfcol_24`,
    `bfcol_15` AS `bfcol_25`,
    `bfcol_16` AS `bfcol_26`,
    `bfcol_17` AS `bfcol_27`,
    `bfcol_18` AS `bfcol_28`,
    TIMESTAMP_ADD(CAST(`bfcol_16` AS DATETIME), INTERVAL 86400000000 MICROSECOND) AS `bfcol_29`
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
    TIMESTAMP_ADD(`bfcol_25`, INTERVAL 86400000000 MICROSECOND) AS `bfcol_42`
  FROM `bfcte_3`
), `bfcte_5` AS (
  SELECT
    *,
    172800000000 AS `bfcol_50`
  FROM `bfcte_4`
)
SELECT
  `bfcol_36` AS `rowindex`,
  `bfcol_37` AS `timestamp_col`,
  `bfcol_38` AS `date_col`,
  `bfcol_39` AS `date_add_timedelta`,
  `bfcol_40` AS `timestamp_add_timedelta`,
  `bfcol_41` AS `timedelta_add_date`,
  `bfcol_42` AS `timedelta_add_timestamp`,
  `bfcol_50` AS `timedelta_add_timedelta`
FROM `bfcte_5`