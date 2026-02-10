SELECT
  `rowindex`,
  `int64_col`,
  `float64_col`,
  CASE
    WHEN `int64_col` = CAST(0 AS INT64)
    THEN CAST(0 AS INT64) * `int64_col`
    WHEN `int64_col` < CAST(0 AS INT64)
    AND (
      MOD(`int64_col`, `int64_col`)
    ) > CAST(0 AS INT64)
    THEN `int64_col` + (
      MOD(`int64_col`, `int64_col`)
    )
    WHEN `int64_col` > CAST(0 AS INT64)
    AND (
      MOD(`int64_col`, `int64_col`)
    ) < CAST(0 AS INT64)
    THEN `int64_col` + (
      MOD(`int64_col`, `int64_col`)
    )
    ELSE MOD(`int64_col`, `int64_col`)
  END AS `int_mod_int`,
  CASE
    WHEN -(
      `int64_col`
    ) = CAST(0 AS INT64)
    THEN CAST(0 AS INT64) * `int64_col`
    WHEN -(
      `int64_col`
    ) < CAST(0 AS INT64)
    AND (
      MOD(`int64_col`, -(
        `int64_col`
      ))
    ) > CAST(0 AS INT64)
    THEN -(
      `int64_col`
    ) + (
      MOD(`int64_col`, -(
        `int64_col`
      ))
    )
    WHEN -(
      `int64_col`
    ) > CAST(0 AS INT64)
    AND (
      MOD(`int64_col`, -(
        `int64_col`
      ))
    ) < CAST(0 AS INT64)
    THEN -(
      `int64_col`
    ) + (
      MOD(`int64_col`, -(
        `int64_col`
      ))
    )
    ELSE MOD(`int64_col`, -(
      `int64_col`
    ))
  END AS `int_mod_int_neg`,
  CASE
    WHEN 1 = CAST(0 AS INT64)
    THEN CAST(0 AS INT64) * `int64_col`
    WHEN 1 < CAST(0 AS INT64) AND (
      MOD(`int64_col`, 1)
    ) > CAST(0 AS INT64)
    THEN 1 + (
      MOD(`int64_col`, 1)
    )
    WHEN 1 > CAST(0 AS INT64) AND (
      MOD(`int64_col`, 1)
    ) < CAST(0 AS INT64)
    THEN 1 + (
      MOD(`int64_col`, 1)
    )
    ELSE MOD(`int64_col`, 1)
  END AS `int_mod_1`,
  CASE
    WHEN 0 = CAST(0 AS INT64)
    THEN CAST(0 AS INT64) * `int64_col`
    WHEN 0 < CAST(0 AS INT64) AND (
      MOD(`int64_col`, 0)
    ) > CAST(0 AS INT64)
    THEN 0 + (
      MOD(`int64_col`, 0)
    )
    WHEN 0 > CAST(0 AS INT64) AND (
      MOD(`int64_col`, 0)
    ) < CAST(0 AS INT64)
    THEN 0 + (
      MOD(`int64_col`, 0)
    )
    ELSE MOD(`int64_col`, 0)
  END AS `int_mod_0`,
  CASE
    WHEN CAST(`float64_col` AS BIGNUMERIC) = CAST(0 AS INT64)
    THEN CAST('NaN' AS FLOAT64) * CAST(`float64_col` AS BIGNUMERIC)
    WHEN CAST(`float64_col` AS BIGNUMERIC) < CAST(0 AS INT64)
    AND (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(`float64_col` AS BIGNUMERIC))
    ) > CAST(0 AS INT64)
    THEN CAST(`float64_col` AS BIGNUMERIC) + (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(`float64_col` AS BIGNUMERIC))
    )
    WHEN CAST(`float64_col` AS BIGNUMERIC) > CAST(0 AS INT64)
    AND (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(`float64_col` AS BIGNUMERIC))
    ) < CAST(0 AS INT64)
    THEN CAST(`float64_col` AS BIGNUMERIC) + (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(`float64_col` AS BIGNUMERIC))
    )
    ELSE MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(`float64_col` AS BIGNUMERIC))
  END AS `float_mod_float`,
  CASE
    WHEN CAST(-(
      `float64_col`
    ) AS BIGNUMERIC) = CAST(0 AS INT64)
    THEN CAST('NaN' AS FLOAT64) * CAST(`float64_col` AS BIGNUMERIC)
    WHEN CAST(-(
      `float64_col`
    ) AS BIGNUMERIC) < CAST(0 AS INT64)
    AND (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(-(
        `float64_col`
      ) AS BIGNUMERIC))
    ) > CAST(0 AS INT64)
    THEN CAST(-(
      `float64_col`
    ) AS BIGNUMERIC) + (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(-(
        `float64_col`
      ) AS BIGNUMERIC))
    )
    WHEN CAST(-(
      `float64_col`
    ) AS BIGNUMERIC) > CAST(0 AS INT64)
    AND (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(-(
        `float64_col`
      ) AS BIGNUMERIC))
    ) < CAST(0 AS INT64)
    THEN CAST(-(
      `float64_col`
    ) AS BIGNUMERIC) + (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(-(
        `float64_col`
      ) AS BIGNUMERIC))
    )
    ELSE MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(-(
      `float64_col`
    ) AS BIGNUMERIC))
  END AS `float_mod_float_neg`,
  CASE
    WHEN CAST(1 AS BIGNUMERIC) = CAST(0 AS INT64)
    THEN CAST('NaN' AS FLOAT64) * CAST(`float64_col` AS BIGNUMERIC)
    WHEN CAST(1 AS BIGNUMERIC) < CAST(0 AS INT64)
    AND (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(1 AS BIGNUMERIC))
    ) > CAST(0 AS INT64)
    THEN CAST(1 AS BIGNUMERIC) + (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(1 AS BIGNUMERIC))
    )
    WHEN CAST(1 AS BIGNUMERIC) > CAST(0 AS INT64)
    AND (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(1 AS BIGNUMERIC))
    ) < CAST(0 AS INT64)
    THEN CAST(1 AS BIGNUMERIC) + (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(1 AS BIGNUMERIC))
    )
    ELSE MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(1 AS BIGNUMERIC))
  END AS `float_mod_1`,
  CASE
    WHEN CAST(0 AS BIGNUMERIC) = CAST(0 AS INT64)
    THEN CAST('NaN' AS FLOAT64) * CAST(`float64_col` AS BIGNUMERIC)
    WHEN CAST(0 AS BIGNUMERIC) < CAST(0 AS INT64)
    AND (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(0 AS BIGNUMERIC))
    ) > CAST(0 AS INT64)
    THEN CAST(0 AS BIGNUMERIC) + (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(0 AS BIGNUMERIC))
    )
    WHEN CAST(0 AS BIGNUMERIC) > CAST(0 AS INT64)
    AND (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(0 AS BIGNUMERIC))
    ) < CAST(0 AS INT64)
    THEN CAST(0 AS BIGNUMERIC) + (
      MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(0 AS BIGNUMERIC))
    )
    ELSE MOD(CAST(`float64_col` AS BIGNUMERIC), CAST(0 AS BIGNUMERIC))
  END AS `float_mod_0`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`