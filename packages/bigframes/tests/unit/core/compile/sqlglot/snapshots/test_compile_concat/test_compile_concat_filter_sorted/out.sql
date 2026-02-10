WITH `bfcte_0` AS (
  SELECT
    `bfcol_6` AS `bfcol_42`,
    `bfcol_7` AS `bfcol_43`,
    `bfcol_8` AS `bfcol_44`,
    `bfcol_9` AS `bfcol_45`
  FROM (
    (
      SELECT
        `float64_col` AS `bfcol_6`,
        `int64_col` AS `bfcol_7`,
        0 AS `bfcol_8`,
        ROW_NUMBER() OVER (ORDER BY `int64_col` ASC NULLS LAST) - 1 AS `bfcol_9`
      FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
    )
    UNION ALL
    (
      SELECT
        `float64_col` AS `bfcol_17`,
        `int64_too` AS `bfcol_18`,
        1 AS `bfcol_19`,
        ROW_NUMBER() OVER () - 1 AS `bfcol_20`
      FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
      WHERE
        `bool_col`
    )
    UNION ALL
    (
      SELECT
        `float64_col` AS `bfcol_27`,
        `int64_col` AS `bfcol_28`,
        2 AS `bfcol_29`,
        ROW_NUMBER() OVER (ORDER BY `int64_col` ASC NULLS LAST) - 1 AS `bfcol_30`
      FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
    )
    UNION ALL
    (
      SELECT
        `float64_col` AS `bfcol_38`,
        `int64_too` AS `bfcol_39`,
        3 AS `bfcol_40`,
        ROW_NUMBER() OVER () - 1 AS `bfcol_41`
      FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
      WHERE
        `bool_col`
    )
  )
)
SELECT
  `bfcol_42` AS `float64_col`,
  `bfcol_43` AS `int64_col`
FROM `bfcte_0`
ORDER BY
  `bfcol_44` ASC NULLS LAST,
  `bfcol_45` ASC NULLS LAST