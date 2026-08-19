SELECT
  ~(
    `int64_col`
  ) AS `int64_col`,
  ~(
    `bytes_col`
  ) AS `bytes_col`,
  NOT (
    `bool_col`
  ) AS `bool_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`