SELECT
  AI.CLASSIFY(
    input => `string_col`,
    categories => ['greeting', 'rejection'],
    examples => [
      STRUCT('hi' AS `input`, ['greeting', 'positive'] AS `output`),
      STRUCT('bye' AS `input`, ['rejection', 'negative'] AS `output`)
    ],
    output_mode => 'multi'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`