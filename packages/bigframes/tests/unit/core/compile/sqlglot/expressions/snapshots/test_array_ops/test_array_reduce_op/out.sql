WITH `bfcte_0` AS (
  SELECT
    `bool_list_col`,
    `float_list_col`,
    `string_list_col`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`
), `bfcte_1` AS (
  SELECT
    *,
    (
      SELECT
        COALESCE(SUM(bf_arr_reduce_uid), 0)
      FROM UNNEST(`float_list_col`) AS bf_arr_reduce_uid
    ) AS `bfcol_3`,
    (
      SELECT
        STDDEV(bf_arr_reduce_uid)
      FROM UNNEST(`float_list_col`) AS bf_arr_reduce_uid
    ) AS `bfcol_4`,
    (
      SELECT
        COUNT(bf_arr_reduce_uid)
      FROM UNNEST(`string_list_col`) AS bf_arr_reduce_uid
    ) AS `bfcol_5`,
    (
      SELECT
        COALESCE(LOGICAL_OR(bf_arr_reduce_uid), FALSE)
      FROM UNNEST(`bool_list_col`) AS bf_arr_reduce_uid
    ) AS `bfcol_6`
  FROM `bfcte_0`
)
SELECT
  `bfcol_3` AS `sum_float`,
  `bfcol_4` AS `std_float`,
  `bfcol_5` AS `count_str`,
  `bfcol_6` AS `any_bool`
FROM `bfcte_1`