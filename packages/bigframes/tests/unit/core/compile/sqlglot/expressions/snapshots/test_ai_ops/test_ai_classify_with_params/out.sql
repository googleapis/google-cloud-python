SELECT
  AI.CLASSIFY(
    input => `string_col`,
    categories => ['greeting', 'rejection'],
    examples => [
      STRUCT('hi' AS `input`, 'greeting' AS `output`),
      STRUCT('bye' AS `input`, 'rejection' AS `output`)
    ],
    endpoint => 'gemini-2.5-flash',
    max_error_ratio => 0.1
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`