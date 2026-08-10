SELECT
  AI.GENERATE_INT(
    prompt => STRUCT(`string_col`, ' is the same as ', `string_col`),
    model_params => JSON '{}'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`