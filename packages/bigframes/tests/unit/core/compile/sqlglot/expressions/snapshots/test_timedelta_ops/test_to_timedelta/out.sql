WITH `bfcte_0` AS (
  SELECT
    `int64_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `rowindex` AS `bfcol_4`,
    `int64_col` AS `bfcol_5`,
    `int64_col` AS `bfcol_6`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_4` AS `bfcol_10`,
    `bfcol_5` AS `bfcol_11`,
    `bfcol_6` AS `bfcol_12`,
    `bfcol_5` * 1000000 AS `bfcol_13`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *,
    `bfcol_10` AS `bfcol_18`,
    `bfcol_11` AS `bfcol_19`,
    `bfcol_12` AS `bfcol_20`,
    `bfcol_13` AS `bfcol_21`,
    `bfcol_11` * 604800000000 AS `bfcol_22`
  FROM `bfcte_2`
)
SELECT
  `bfcol_18` AS `rowindex`,
  `bfcol_19` AS `int64_col`,
  `bfcol_20` AS `duration_us`,
  `bfcol_21` AS `duration_s`,
  `bfcol_22` AS `duration_w`
FROM `bfcte_3`