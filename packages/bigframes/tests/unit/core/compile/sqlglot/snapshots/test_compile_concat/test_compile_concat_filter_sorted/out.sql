WITH `bfcte_0` AS (
  SELECT
    `float64_col` AS `bfcol_7`,
    `int64_too` AS `bfcol_8`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
  WHERE
    `bool_col`
), `bfcte_1` AS (
  SELECT
    `float64_col` AS `bfcol_5`,
    `int64_col` AS `bfcol_6`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
), `bfcte_2` AS (
  SELECT
    `bfcol_21` AS `bfcol_33`,
    `bfcol_22` AS `bfcol_34`,
    `bfcol_23` AS `bfcol_35`,
    `bfcol_24` AS `bfcol_36`
  FROM (
    (
      SELECT
        `bfcol_5` AS `bfcol_21`,
        `bfcol_6` AS `bfcol_22`,
        0 AS `bfcol_23`,
        ROW_NUMBER() OVER (ORDER BY `bfcol_6` ASC NULLS LAST) - 1 AS `bfcol_24`
      FROM `bfcte_1`
    )
    UNION ALL
    (
      SELECT
        `bfcol_7` AS `bfcol_29`,
        `bfcol_8` AS `bfcol_30`,
        1 AS `bfcol_31`,
        ROW_NUMBER() OVER () - 1 AS `bfcol_32`
      FROM `bfcte_0`
    )
    UNION ALL
    (
      SELECT
        `bfcol_5` AS `bfcol_17`,
        `bfcol_6` AS `bfcol_18`,
        2 AS `bfcol_19`,
        ROW_NUMBER() OVER (ORDER BY `bfcol_6` ASC NULLS LAST) - 1 AS `bfcol_20`
      FROM `bfcte_1`
    )
    UNION ALL
    (
      SELECT
        `bfcol_7` AS `bfcol_25`,
        `bfcol_8` AS `bfcol_26`,
        3 AS `bfcol_27`,
        ROW_NUMBER() OVER () - 1 AS `bfcol_28`
      FROM `bfcte_0`
    )
  )
)
SELECT
  `bfcol_33` AS `float64_col`,
  `bfcol_34` AS `int64_col`
FROM `bfcte_2`
ORDER BY
  `bfcol_35` ASC NULLS LAST,
  `bfcol_36` ASC NULLS LAST