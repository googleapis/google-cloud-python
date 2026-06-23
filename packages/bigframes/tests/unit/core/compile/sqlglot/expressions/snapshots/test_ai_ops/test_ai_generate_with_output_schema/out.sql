SELECT
  AI.GENERATE(
    prompt => STRUCT(`string_col`, ' is the same as ', `string_col`),
    endpoint => 'gemini-3.1-flash-lite',
    output_schema => 'x INT64, y FLOAT64'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
