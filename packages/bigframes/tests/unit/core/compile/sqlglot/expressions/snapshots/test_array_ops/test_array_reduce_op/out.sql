SELECT
  (
    SELECT
      COALESCE(SUM(bf_arr_reduce_uid), 0)
    FROM UNNEST(`float_list_col`) AS bf_arr_reduce_uid
  ) AS `sum_float`,
  (
    SELECT
      STDDEV(bf_arr_reduce_uid)
    FROM UNNEST(`float_list_col`) AS bf_arr_reduce_uid
  ) AS `std_float`,
  (
    SELECT
      COUNT(bf_arr_reduce_uid)
    FROM UNNEST(`string_list_col`) AS bf_arr_reduce_uid
  ) AS `count_str`,
  (
    SELECT
      COALESCE(LOGICAL_OR(bf_arr_reduce_uid), FALSE)
    FROM UNNEST(`bool_list_col`) AS bf_arr_reduce_uid
  ) AS `any_bool`
FROM `bigframes-dev`.`sqlglot_test`.`repeated_types` AS `bft_0`