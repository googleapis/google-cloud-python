SELECT
  AI.CLASSIFY(
    input => (`string_col`),
    categories => ['greeting', 'rejection'],
    examples => [('hi', 'greeting'), ('bye', 'rejection')],
    endpoint => 'gemini-2.5-flash',
    max_error_ratio => 0.1
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`