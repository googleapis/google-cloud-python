WITH `bfcte_0` AS (
  SELECT
    `string_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    AI.GENERATE_BOOL(
      prompt => (`bfcol_0`, ' is the same as ', `bfcol_0`),
      connection_id => 'test_connection_id',
      endpoint => 'gemini-2.5-flash',
      request_type => 'SHARED'
    ) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `result`
FROM `bfcte_1`