SELECT
  `int64_col`,
  COALESCE(`int64_too`, `int64_col`) AS `int64_too`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`