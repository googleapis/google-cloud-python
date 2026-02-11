SELECT
  `rowindex`,
  `int64_col`,
  IF(
    (
      `int64_col`
    ) IS NOT NULL,
    IF(
      `int64_col` IS NULL,
      NULL,
      CAST(GREATEST(
        CEIL(
          PERCENT_RANK() OVER (PARTITION BY (
            `int64_col`
          ) IS NOT NULL ORDER BY `int64_col` ASC) * 4
        ) - 1,
        0
      ) AS INT64)
    ),
    NULL
  ) AS `qcut_w_int`,
  IF(
    (
      `int64_col`
    ) IS NOT NULL,
    CASE
      WHEN PERCENT_RANK() OVER (PARTITION BY (
        `int64_col`
      ) IS NOT NULL ORDER BY `int64_col` ASC) < 0
      THEN NULL
      WHEN PERCENT_RANK() OVER (PARTITION BY (
        `int64_col`
      ) IS NOT NULL ORDER BY `int64_col` ASC) <= 0.25
      THEN 0
      WHEN PERCENT_RANK() OVER (PARTITION BY (
        `int64_col`
      ) IS NOT NULL ORDER BY `int64_col` ASC) <= 0.5
      THEN 1
      WHEN PERCENT_RANK() OVER (PARTITION BY (
        `int64_col`
      ) IS NOT NULL ORDER BY `int64_col` ASC) <= 0.75
      THEN 2
      WHEN PERCENT_RANK() OVER (PARTITION BY (
        `int64_col`
      ) IS NOT NULL ORDER BY `int64_col` ASC) <= 1
      THEN 3
      ELSE NULL
    END,
    NULL
  ) AS `qcut_w_list`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`