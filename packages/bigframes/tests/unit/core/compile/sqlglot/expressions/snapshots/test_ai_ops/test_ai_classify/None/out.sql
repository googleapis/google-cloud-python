SELECT
  AI.CLASSIFY(input => (`string_col`), categories => ['greeting', 'rejection']) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`