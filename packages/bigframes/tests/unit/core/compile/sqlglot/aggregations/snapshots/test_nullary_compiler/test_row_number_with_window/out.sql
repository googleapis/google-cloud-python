SELECT
  ROW_NUMBER() OVER (ORDER BY `int64_col` ASC NULLS LAST) - 1 AS `row_number`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`