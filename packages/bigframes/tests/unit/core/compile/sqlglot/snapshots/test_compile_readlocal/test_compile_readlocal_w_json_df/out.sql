WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` INT64, `bfcol_1` JSON, `bfcol_2` INT64>>[STRUCT(0, PARSE_JSON('null'), 0), STRUCT(1, PARSE_JSON('true'), 1), STRUCT(2, PARSE_JSON('100'), 2), STRUCT(3, PARSE_JSON('0.98'), 3), STRUCT(4, PARSE_JSON('"a string"'), 4), STRUCT(5, PARSE_JSON('[]'), 5), STRUCT(6, PARSE_JSON('[1,2,3]'), 6), STRUCT(7, PARSE_JSON('[{"a":1},{"a":2},{"a":null},{}]'), 7), STRUCT(8, PARSE_JSON('"100"'), 8), STRUCT(9, PARSE_JSON('{"date":"2024-07-16"}'), 9), STRUCT(10, PARSE_JSON('{"int_value":2,"null_filed":null}'), 10), STRUCT(11, PARSE_JSON('{"list_data":[10,20,30]}'), 11)])
)
SELECT
  `bfcol_0` AS `rowindex`,
  `bfcol_1` AS `json_col`
FROM `bfcte_0`
ORDER BY
  `bfcol_2` ASC NULLS LAST