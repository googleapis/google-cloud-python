SELECT
  AI.CLASSIFY(
    input => STRUCT(`string_col`),
    categories => ['greeting', 'rejection'],
    examples => [('hi', 'greeting'), ('bye', 'rejection')],
    endpoint => 'gemini-3.5-flash',
    max_error_ratio => 0.1
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`