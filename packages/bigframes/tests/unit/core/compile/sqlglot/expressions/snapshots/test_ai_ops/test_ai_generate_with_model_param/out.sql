SELECT
  AI.GENERATE(
    prompt => (`string_col`, ' is the same as ', `string_col`),
    request_type => 'SHARED',
    model_params => JSON '{}'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`