SELECT
  DATETIME_DIFF(
    `datetime_col`,
    LAG(`datetime_col`, 1) OVER (ORDER BY `datetime_col` ASC NULLS LAST),
    MICROSECOND
  ) AS `diff_datetime`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`