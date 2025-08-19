WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`,
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
    INTERVAL `bfcol_3` MICROSECOND AS `bfcol_11`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_8` AS `bfcol_16`,
    `bfcol_9` AS `bfcol_17`,
    `bfcol_10` AS `bfcol_18`,
    `bfcol_11` AS `bfcol_19`,
    CAST(FLOOR(`bfcol_11` * `bfcol_10`) AS INT64) AS `bfcol_20`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *,
    `bfcol_16` AS `bfcol_26`,
    `bfcol_17` AS `bfcol_27`,
    `bfcol_18` AS `bfcol_28`,
    `bfcol_19` AS `bfcol_29`,
    `bfcol_20` AS `bfcol_30`,
    CAST(FLOOR(`bfcol_18` * `bfcol_19`) AS INT64) AS `bfcol_31`
  FROM `bfcte_2`
)
SELECT
  `bfcol_26` AS `rowindex`,
  `bfcol_27` AS `timestamp_col`,
  `bfcol_28` AS `int64_col`,
  `bfcol_29` AS `duration_col`,
  `bfcol_30` AS `timedelta_mul_numeric`,
  `bfcol_31` AS `numeric_mul_timedelta`
FROM `bfcte_3`