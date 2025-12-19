WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `int64_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `rowindex` AS `bfcol_6`,
    `bool_col` AS `bfcol_7`,
    `int64_col` AS `bfcol_8`,
    `bool_col` AS `bfcol_9`
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
        ORDER BY `bfcol_9` ASC NULLS LAST, `rowindex` ASC NULLS LAST
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
      ) < 3
      THEN NULL
      ELSE COALESCE(
        SUM(CAST(`bfcol_7` AS INT64)) OVER (
          PARTITION BY `bfcol_9`
          ORDER BY `bfcol_9` ASC NULLS LAST, `rowindex` ASC NULLS LAST
          ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
        ),
        0
      )
    END AS `bfcol_15`
  FROM `bfcte_2`
), `bfcte_4` AS (
  SELECT
    *,
    CASE
      WHEN SUM(CAST(NOT `bfcol_8` IS NULL AS INT64)) OVER (
        PARTITION BY `bfcol_9`
        ORDER BY `bfcol_9` ASC NULLS LAST, `rowindex` ASC NULLS LAST
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
      ) < 3
      THEN NULL
      ELSE COALESCE(
        SUM(`bfcol_8`) OVER (
          PARTITION BY `bfcol_9`
          ORDER BY `bfcol_9` ASC NULLS LAST, `rowindex` ASC NULLS LAST
          ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
        ),
        0
      )
    END AS `bfcol_16`
  FROM `bfcte_3`
)
SELECT
  `bfcol_9` AS `bool_col`,
  `bfcol_6` AS `rowindex`,
  `bfcol_15` AS `bool_col_1`,
  `bfcol_16` AS `int64_col`
FROM `bfcte_4`
ORDER BY
  `bfcol_9` ASC NULLS LAST,
  `rowindex` ASC NULLS LAST