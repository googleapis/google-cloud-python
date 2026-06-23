SELECT
  AI.SCORE(
    prompt => STRUCT(`string_col`, ' is the same as ', `string_col`),
    endpoint => 'gemini-3.1-flash-lite',
    max_error_ratio => 0.5
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
