SELECT
  AI.IF(
    prompt => (`string_col`, ' is the same as ', `string_col`),
    connection_id => 'bigframes-dev.us.bigframes-default-connection'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`