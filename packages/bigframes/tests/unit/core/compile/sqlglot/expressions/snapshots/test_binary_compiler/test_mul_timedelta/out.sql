WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`,
    `rowindex` AS `bfcol_1`,
    `timestamp_col` AS `bfcol_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bfcol_1` AS `bfcol_6`,
    `bfcol_2` AS `bfcol_7`,
    `bfcol_0` AS `bfcol_8`,
    CAST(FLOOR(86400000000 * `bfcol_0`) AS INT64) AS `bfcol_9`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_6` AS `bfcol_14`,
    `bfcol_7` AS `bfcol_15`,
    `bfcol_8` AS `bfcol_16`,
    `bfcol_9` AS `bfcol_17`,
    CAST(FLOOR(`bfcol_8` * 86400000000) AS INT64) AS `bfcol_18`
  FROM `bfcte_1`
)
SELECT
  `bfcol_14` AS `rowindex`,
  `bfcol_15` AS `timestamp_col`,
  `bfcol_16` AS `int64_col`,
  `bfcol_17` AS `timedelta_mul_numeric`,
  `bfcol_18` AS `numeric_mul_timedelta`
FROM `bfcte_2`