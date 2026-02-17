WITH `bfcte_0` AS (
  SELECT
    `bfcol_9` AS `bfcol_30`,
    `bfcol_10` AS `bfcol_31`,
    `bfcol_11` AS `bfcol_32`,
    `bfcol_12` AS `bfcol_33`,
    `bfcol_13` AS `bfcol_34`,
    `bfcol_14` AS `bfcol_35`
  FROM (
    (
      SELECT
        `rowindex` AS `bfcol_9`,
        `rowindex` AS `bfcol_10`,
        `int64_col` AS `bfcol_11`,
        `string_col` AS `bfcol_12`,
        0 AS `bfcol_13`,
        ROW_NUMBER() OVER () - 1 AS `bfcol_14`
      FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
    )
    UNION ALL
    (
      SELECT
        `rowindex` AS `bfcol_24`,
        `rowindex` AS `bfcol_25`,
        `int64_col` AS `bfcol_26`,
        `string_col` AS `bfcol_27`,
        1 AS `bfcol_28`,
        ROW_NUMBER() OVER () - 1 AS `bfcol_29`
      FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
    )
  )
)
SELECT
  `bfcol_30` AS `rowindex`,
  `bfcol_31` AS `rowindex_1`,
  `bfcol_32` AS `int64_col`,
  `bfcol_33` AS `string_col`
FROM `bfcte_0`
ORDER BY
  `bfcol_34` ASC NULLS LAST,
  `bfcol_35` ASC NULLS LAST