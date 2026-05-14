SELECT
  AI.GENERATE(
    prompt => (`string_col`, ' is the same as ', `string_col`),
    endpoint => 'gemini-2.5-flash',
    request_type => 'SHARED'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`