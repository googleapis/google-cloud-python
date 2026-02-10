SELECT
  `rowindex`,
  `timestamp_col`,
  `date_col`,
  43200000000 AS `timedelta_div_numeric`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`