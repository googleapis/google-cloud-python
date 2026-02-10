SELECT
  `rowindex`,
  CASE
    WHEN COALESCE(
      SUM(CAST(NOT (
        `int64_col`
      ) IS NULL AS INT64)) OVER (ORDER BY `rowindex` ASC NULLS LAST ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),
      0
    ) < 3
    THEN NULL
    WHEN TRUE
    THEN COALESCE(
      SUM(`int64_col`) OVER (ORDER BY `rowindex` ASC NULLS LAST ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),
      0
    )
  END AS `int64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
ORDER BY
  `rowindex` ASC NULLS LAST