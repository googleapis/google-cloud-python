WITH `bfcte_1` AS (
  SELECT
    `int64_col`,
    `rowindex`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_3` AS (
  SELECT
    *,
    ROW_NUMBER() OVER () - 1 AS `bfcol_7`
  FROM `bfcte_1`
), `bfcte_5` AS (
  SELECT
    *,
    0 AS `bfcol_8`
  FROM `bfcte_3`
), `bfcte_6` AS (
  SELECT
    `rowindex` AS `bfcol_9`,
    `rowindex` AS `bfcol_10`,
    `int64_col` AS `bfcol_11`,
    `string_col` AS `bfcol_12`,
    `bfcol_8` AS `bfcol_13`,
    `bfcol_7` AS `bfcol_14`
  FROM `bfcte_5`
), `bfcte_0` AS (
  SELECT
    `int64_col`,
    `rowindex`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_2` AS (
  SELECT
    *,
    ROW_NUMBER() OVER () - 1 AS `bfcol_22`
  FROM `bfcte_0`
), `bfcte_4` AS (
  SELECT
    *,
    1 AS `bfcol_23`
  FROM `bfcte_2`
), `bfcte_7` AS (
  SELECT
    `rowindex` AS `bfcol_24`,
    `rowindex` AS `bfcol_25`,
    `int64_col` AS `bfcol_26`,
    `string_col` AS `bfcol_27`,
    `bfcol_23` AS `bfcol_28`,
    `bfcol_22` AS `bfcol_29`
  FROM `bfcte_4`
), `bfcte_8` AS (
  SELECT
    *
  FROM (
    SELECT
      `bfcol_9` AS `bfcol_30`,
      `bfcol_10` AS `bfcol_31`,
      `bfcol_11` AS `bfcol_32`,
      `bfcol_12` AS `bfcol_33`,
      `bfcol_13` AS `bfcol_34`,
      `bfcol_14` AS `bfcol_35`
    FROM `bfcte_6`
    UNION ALL
    SELECT
      `bfcol_24` AS `bfcol_30`,
      `bfcol_25` AS `bfcol_31`,
      `bfcol_26` AS `bfcol_32`,
      `bfcol_27` AS `bfcol_33`,
      `bfcol_28` AS `bfcol_34`,
      `bfcol_29` AS `bfcol_35`
    FROM `bfcte_7`
  )
)
SELECT
  `bfcol_30` AS `rowindex`,
  `bfcol_31` AS `rowindex_1`,
  `bfcol_32` AS `int64_col`,
  `bfcol_33` AS `string_col`
FROM `bfcte_8`
ORDER BY
  `bfcol_34` ASC NULLS LAST,
  `bfcol_35` ASC NULLS LAST