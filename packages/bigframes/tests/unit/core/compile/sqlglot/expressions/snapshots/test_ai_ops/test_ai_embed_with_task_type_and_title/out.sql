SELECT
  AI.EMBED(
    `string_col`,
    endpoint => 'text-embedding-005',
    task_type => 'RETRIEVAL_DOCUMENT',
    title => 'My Document',
    model_params => JSON '{"outputDimensionality": 256}'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`