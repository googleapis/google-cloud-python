SELECT
  AI.CLASSIFY(
    input => (`string_col`),
    categories => ['greeting', 'rejection'],
    connection_id => 'bigframes-dev.us.bigframes-default-connection'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`