SELECT
  `rowindex`,
  OBJ.FETCH_METADATA(
    OBJ.MAKE_REF(`string_col`, 'bigframes-dev.test-region.bigframes-default-connection')
  ).`version`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`