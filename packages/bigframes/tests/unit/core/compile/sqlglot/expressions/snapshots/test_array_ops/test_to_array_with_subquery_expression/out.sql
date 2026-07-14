SELECT
  [
    COALESCE(
      (
        SELECT
          COALESCE(SUM(bf_arr_reduce_uid), 0)
        FROM UNNEST(`float_list_col`) AS bf_arr_reduce_uid
      ),
      0.0
    )
  ] AS `arr_subquery_coalesce`
FROM `bigframes-dev`.`sqlglot_test`.`repeated_types` AS `bft_0`
