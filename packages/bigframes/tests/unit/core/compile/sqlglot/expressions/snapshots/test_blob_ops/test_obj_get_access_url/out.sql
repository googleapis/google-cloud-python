SELECT
  `rowindex`,
  JSON_VALUE(
    OBJ.GET_ACCESS_URL(
      OBJ.MAKE_REF(`string_col`, 'bigframes-dev.test-region.bigframes-default-connection'),
      'R'
    ),
    '$.access_urls.read_url'
  ) AS `string_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`