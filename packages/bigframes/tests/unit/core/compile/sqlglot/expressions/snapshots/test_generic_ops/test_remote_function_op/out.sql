SELECT
  `my_project`.`my_dataset`.`my_routine`(`int64_col`) AS `apply_on_null_true`,
  IF(
    `int64_col` IS NULL,
    `int64_col`,
    `my_project`.`my_dataset`.`my_routine`(`int64_col`)
  ) AS `apply_on_null_false`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`