SELECT
  `rowindex`,
  CASE
    WHEN COUNT(NOT (
      `int64_col`
    ) IS NULL) OVER (ORDER BY `rowindex` ASC NULLS LAST ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) < 5
    THEN NULL
    WHEN TRUE
    THEN COUNT(`int64_col`) OVER (ORDER BY `rowindex` ASC NULLS LAST ROWS BETWEEN 4 PRECEDING AND CURRENT ROW)
  END AS `int64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
ORDER BY
  `rowindex` ASC NULLS LAST