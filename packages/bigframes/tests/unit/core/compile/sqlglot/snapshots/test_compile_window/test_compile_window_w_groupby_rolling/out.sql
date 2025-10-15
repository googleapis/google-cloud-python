WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `int64_col` AS `bfcol_1`,
    `rowindex` AS `bfcol_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bfcol_2` AS `bfcol_6`,
    `bfcol_0` AS `bfcol_7`,
    `bfcol_1` AS `bfcol_8`,
    `bfcol_0` AS `bfcol_9`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *
  FROM `bfcte_1`
  WHERE
    NOT `bfcol_9` IS NULL
), `bfcte_3` AS (
  SELECT
    *,
    CASE
      WHEN SUM(CAST(NOT `bfcol_7` IS NULL AS INT64)) OVER (
        PARTITION BY `bfcol_9`
        ORDER BY `bfcol_9` ASC NULLS LAST, `bfcol_2` ASC NULLS LAST
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
      ) < 3
      THEN NULL
      ELSE COALESCE(
        SUM(CAST(`bfcol_7` AS INT64)) OVER (
          PARTITION BY `bfcol_9`
          ORDER BY `bfcol_9` ASC NULLS LAST, `bfcol_2` ASC NULLS LAST
          ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
        ),
        0
      )
    END AS `bfcol_15`
  FROM `bfcte_2`
), `bfcte_4` AS (
  SELECT
    *
  FROM `bfcte_3`
  WHERE
    NOT `bfcol_9` IS NULL
), `bfcte_5` AS (
  SELECT
    *,
    CASE
      WHEN SUM(CAST(NOT `bfcol_8` IS NULL AS INT64)) OVER (
        PARTITION BY `bfcol_9`
        ORDER BY `bfcol_9` ASC NULLS LAST, `bfcol_2` ASC NULLS LAST
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
      ) < 3
      THEN NULL
      ELSE COALESCE(
        SUM(`bfcol_8`) OVER (
          PARTITION BY `bfcol_9`
          ORDER BY `bfcol_9` ASC NULLS LAST, `bfcol_2` ASC NULLS LAST
          ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
        ),
        0
      )
    END AS `bfcol_21`
  FROM `bfcte_4`
)
SELECT
  `bfcol_9` AS `bool_col`,
  `bfcol_6` AS `rowindex`,
  `bfcol_15` AS `bool_col_1`,
  `bfcol_21` AS `int64_col`
FROM `bfcte_5`
ORDER BY
  `bfcol_9` ASC NULLS LAST,
  `bfcol_2` ASC NULLS LAST