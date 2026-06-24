SELECT
  AI.GENERATE(
    prompt => STRUCT(`string_col`, ' is the same as ', `string_col`),
    endpoint => 'gemini-3.5-flash',
    request_type => 'SHARED'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`