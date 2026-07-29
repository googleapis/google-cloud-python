SELECT
  SUBSTRING(`string_col`, 2, 4) AS `string_slice`,
  ARRAY(
    SELECT
      el
    FROM UNNEST([`int64_col`, `int64_too`]) AS el WITH OFFSET AS slice_idx
    WHERE
      slice_idx >= 1
  ) AS `slice_only_start`,
  ARRAY(
    SELECT
      el
    FROM UNNEST([`int64_col`, `int64_too`]) AS el WITH OFFSET AS slice_idx
    WHERE
      slice_idx >= 1 AND slice_idx < 5
  ) AS `slice_start_stop`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`