SELECT
  AI.GENERATE_BOOL(
    prompt => STRUCT(`string_col`, ' is the same as ', `string_col`),
    connection_id => 'bigframes-dev.us.bigframes-default-connection',
    endpoint => 'gemini-3.5-flash'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`