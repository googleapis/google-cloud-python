SELECT
  ARRAY(
    SELECT
      el
    FROM UNNEST(`string_list_col`) AS el WITH OFFSET AS slice_idx
    WHERE
      slice_idx >= 1 AND slice_idx < 5
  ) AS `string_list_col`
FROM `bigframes-dev`.`sqlglot_test`.`repeated_types` AS `bft_0`