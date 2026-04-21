SELECT
  AI.EMBED(
    `string_col`,
    connection_id => 'bigframes-dev.us.bigframes-default-connection',
    endpoint => 'text-embedding-005'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`