WITH `bfcte_2` AS (
  SELECT
    `float64_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_6` AS (
  SELECT
    *,
    ROW_NUMBER() OVER (ORDER BY `int64_col` ASC NULLS LAST) - 1 AS `bfcol_4`
  FROM `bfcte_2`
), `bfcte_10` AS (
  SELECT
    *,
    0 AS `bfcol_5`
  FROM `bfcte_6`
), `bfcte_0` AS (
  SELECT
    `bool_col`,
    `float64_col`,
    `int64_too`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_4` AS (
  SELECT
    *
  FROM `bfcte_0`
  WHERE
    `bool_col`
), `bfcte_8` AS (
  SELECT
    *,
    ROW_NUMBER() OVER () - 1 AS `bfcol_15`
  FROM `bfcte_4`
), `bfcte_12` AS (
  SELECT
    *,
    1 AS `bfcol_16`
  FROM `bfcte_8`
), `bfcte_1` AS (
  SELECT
    `float64_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_5` AS (
  SELECT
    *,
    ROW_NUMBER() OVER (ORDER BY `int64_col` ASC NULLS LAST) - 1 AS `bfcol_25`
  FROM `bfcte_1`
), `bfcte_9` AS (
  SELECT
    *,
    2 AS `bfcol_26`
  FROM `bfcte_5`
), `bfcte_0` AS (
  SELECT
    `bool_col`,
    `float64_col`,
    `int64_too`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_3` AS (
  SELECT
    *
  FROM `bfcte_0`
  WHERE
    `bool_col`
), `bfcte_7` AS (
  SELECT
    *,
    ROW_NUMBER() OVER () - 1 AS `bfcol_36`
  FROM `bfcte_3`
), `bfcte_11` AS (
  SELECT
    *,
    3 AS `bfcol_37`
  FROM `bfcte_7`
), `bfcte_13` AS (
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
        `bfcol_5` AS `bfcol_8`,
        `bfcol_4` AS `bfcol_9`
      FROM `bfcte_10`
    )
    UNION ALL
    (
      SELECT
        `float64_col` AS `bfcol_17`,
        `int64_too` AS `bfcol_18`,
        `bfcol_16` AS `bfcol_19`,
        `bfcol_15` AS `bfcol_20`
      FROM `bfcte_12`
    )
    UNION ALL
    (
      SELECT
        `float64_col` AS `bfcol_27`,
        `int64_col` AS `bfcol_28`,
        `bfcol_26` AS `bfcol_29`,
        `bfcol_25` AS `bfcol_30`
      FROM `bfcte_9`
    )
    UNION ALL
    (
      SELECT
        `float64_col` AS `bfcol_38`,
        `int64_too` AS `bfcol_39`,
        `bfcol_37` AS `bfcol_40`,
        `bfcol_36` AS `bfcol_41`
      FROM `bfcte_11`
    )
  )
)
SELECT
  `bfcol_42` AS `float64_col`,
  `bfcol_43` AS `int64_col`
FROM `bfcte_13`
ORDER BY
  `bfcol_44` ASC NULLS LAST,
  `bfcol_45` ASC NULLS LAST