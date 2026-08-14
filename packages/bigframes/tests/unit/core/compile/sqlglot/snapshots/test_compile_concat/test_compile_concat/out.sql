WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_3`,
    `rowindex` AS `bfcol_4`,
    `int64_col` AS `bfcol_5`,
    `string_col` AS `bfcol_6`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
), `bfcte_1` AS (
  SELECT
    `bfcol_17` AS `bfcol_23`,
    `bfcol_18` AS `bfcol_24`,
    `bfcol_19` AS `bfcol_25`,
    `bfcol_20` AS `bfcol_26`,
    `bfcol_21` AS `bfcol_27`,
    `bfcol_22` AS `bfcol_28`
  FROM (
    (
      SELECT
        `bfcol_3` AS `bfcol_17`,
        `bfcol_4` AS `bfcol_18`,
        `bfcol_5` AS `bfcol_19`,
        `bfcol_6` AS `bfcol_20`,
        0 AS `bfcol_21`,
        ROW_NUMBER() OVER () - 1 AS `bfcol_22`
      FROM `bfcte_0`
    )
    UNION ALL
    (
      SELECT
        `bfcol_3` AS `bfcol_11`,
        `bfcol_4` AS `bfcol_12`,
        `bfcol_5` AS `bfcol_13`,
        `bfcol_6` AS `bfcol_14`,
        1 AS `bfcol_15`,
        ROW_NUMBER() OVER () - 1 AS `bfcol_16`
      FROM `bfcte_0`
    )
  )
)
SELECT
  `bfcol_23` AS `rowindex`,
  `bfcol_24` AS `rowindex_1`,
  `bfcol_25` AS `int64_col`,
  `bfcol_26` AS `string_col`
FROM `bfcte_1`
ORDER BY
  `bfcol_27` ASC NULLS LAST,
  `bfcol_28` ASC NULLS LAST