WITH `bfcte_0` AS (
  SELECT
    `int64_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE
      WHEN COALESCE(
        SUM(CAST(NOT `int64_col` IS NULL AS INT64)) OVER (ORDER BY `rowindex` ASC NULLS LAST ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),
        0
      ) < 3
      THEN NULL
      ELSE COALESCE(
        SUM(`int64_col`) OVER (ORDER BY `rowindex` ASC NULLS LAST ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),
        0
      )
    END AS `bfcol_4`
  FROM `bfcte_0`
)
SELECT
  `rowindex`,
  `bfcol_4` AS `int64_col`
FROM `bfcte_1`
ORDER BY
  `rowindex` ASC NULLS LAST