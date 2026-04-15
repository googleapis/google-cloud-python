SELECT
  `rowindex`,
  OBJ.GET_ACCESS_URL(OBJ.MAKE_REF(`string_col`, 'my-connection'), 'r') AS `string_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
