SELECT
  `bool_col`,
  `rowindex`,
  CASE
    WHEN COALESCE(
      SUM(CAST(NOT (
        `bool_col`
      ) IS NULL AS INT64)) OVER (
        PARTITION BY `bool_col`
        ORDER BY `bool_col` ASC NULLS LAST, `rowindex` ASC NULLS LAST
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
      ),
      0
    ) < 3
    THEN NULL
    WHEN TRUE
    THEN COALESCE(
      SUM(CAST(`bool_col` AS INT64)) OVER (
        PARTITION BY `bool_col`
        ORDER BY `bool_col` ASC NULLS LAST, `rowindex` ASC NULLS LAST
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
      ),
      0
    )
  END AS `bool_col_1`,
  CASE
    WHEN COALESCE(
      SUM(CAST(NOT (
        `int64_col`
      ) IS NULL AS INT64)) OVER (
        PARTITION BY `bool_col`
        ORDER BY `bool_col` ASC NULLS LAST, `rowindex` ASC NULLS LAST
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
      ),
      0
    ) < 3
    THEN NULL
    WHEN TRUE
    THEN COALESCE(
      SUM(`int64_col`) OVER (
        PARTITION BY `bool_col`
        ORDER BY `bool_col` ASC NULLS LAST, `rowindex` ASC NULLS LAST
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
      ),
      0
    )
  END AS `int64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
WHERE
  NOT (
    `bool_col`
  ) IS NULL
ORDER BY
  `bool_col` ASC NULLS LAST,
  `rowindex` ASC NULLS LAST