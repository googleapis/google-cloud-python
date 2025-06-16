WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` JSON, `bfcol_1` INT64>>[STRUCT(PARSE_JSON('null'), 0), STRUCT(PARSE_JSON('true'), 1), STRUCT(PARSE_JSON('100'), 2), STRUCT(PARSE_JSON('0.98'), 3), STRUCT(PARSE_JSON('"a string"'), 4), STRUCT(PARSE_JSON('[]'), 5), STRUCT(PARSE_JSON('[1,2,3]'), 6), STRUCT(PARSE_JSON('[{"a":1},{"a":2},{"a":null},{}]'), 7), STRUCT(PARSE_JSON('"100"'), 8), STRUCT(PARSE_JSON('{"date":"2024-07-16"}'), 9), STRUCT(PARSE_JSON('{"int_value":2,"null_filed":null}'), 10), STRUCT(PARSE_JSON('{"list_data":[10,20,30]}'), 11)])
), `bfcte_1` AS (
  SELECT
    `bfcol_0` AS `bfcol_2`,
    `bfcol_1` AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `json_col`
FROM `bfcte_1`
ORDER BY
  `bfcol_3` ASC NULLS LAST