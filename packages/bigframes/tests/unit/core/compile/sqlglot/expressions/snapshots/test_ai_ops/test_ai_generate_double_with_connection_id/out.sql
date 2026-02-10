SELECT
  AI.GENERATE_DOUBLE(
    prompt => (`string_col`, ' is the same as ', `string_col`),
    connection_id => 'bigframes-dev.us.bigframes-default-connection',
    endpoint => 'gemini-2.5-flash',
    request_type => 'SHARED'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`