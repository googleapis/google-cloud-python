SELECT
  AI.CLASSIFY(
    input => STRUCT(`string_col`),
    categories => ['greeting', 'rejection'],
    examples => [('hi', ['greeting', 'positive']), ('bye', ['rejection', 'negative'])],
    output_mode => 'multi'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`