WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`,
    `rowindex` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE
      WHEN SUM(CAST(NOT `bfcol_0` IS NULL AS INT64)) OVER (
        ORDER BY `bfcol_1` IS NULL ASC NULLS LAST, `bfcol_1` ASC NULLS LAST
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
      ) < 3
      THEN NULL
      ELSE COALESCE(
        SUM(`bfcol_0`) OVER (
          ORDER BY `bfcol_1` IS NULL ASC NULLS LAST, `bfcol_1` ASC NULLS LAST
          ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        0
      )
    END AS `bfcol_4`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `rowindex`,
  `bfcol_4` AS `int64_col`
FROM `bfcte_1`
ORDER BY
  `bfcol_1` ASC NULLS LAST