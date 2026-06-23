SELECT
  AI.GENERATE_DOUBLE(
    prompt => STRUCT(`string_col`, ' is the same as ', `string_col`),
    connection_id => 'bigframes-dev.us.bigframes-default-connection',
    endpoint => 'gemini-3.1-flash-lite'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
