SELECT
  `rowindex`,
  `int64_col`,
  `float64_col`,
  CASE
    WHEN `int64_col` <> 0 AND `int64_col` * LN(ABS(`int64_col`)) > 43.66827237527655
    THEN NULL
    ELSE CAST(POWER(CAST(`int64_col` AS NUMERIC), `int64_col`) AS INT64)
  END AS `int_pow_int`,
  CASE
    WHEN `float64_col` = CAST(0 AS INT64)
    THEN 1
    WHEN `int64_col` = 1
    THEN 1
    WHEN `int64_col` = CAST(0 AS INT64) AND `float64_col` < CAST(0 AS INT64)
    THEN CAST('Infinity' AS FLOAT64)
    WHEN ABS(`int64_col`) = CAST('Infinity' AS FLOAT64)
    THEN POWER(
      `int64_col`,
      CASE
        WHEN ABS(`float64_col`) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(`float64_col`)
        ELSE `float64_col`
      END
    )
    WHEN ABS(`float64_col`) > 9007199254740992
    THEN POWER(
      `int64_col`,
      CASE
        WHEN ABS(`float64_col`) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(`float64_col`)
        ELSE `float64_col`
      END
    )
    WHEN `int64_col` < CAST(0 AS INT64)
    AND NOT (
      CAST(`float64_col` AS INT64) = `float64_col`
    )
    THEN CAST('NaN' AS FLOAT64)
    WHEN `int64_col` <> CAST(0 AS INT64) AND `float64_col` * LN(ABS(`int64_col`)) > 709.78
    THEN CAST('Infinity' AS FLOAT64) * CASE
      WHEN `int64_col` < CAST(0 AS INT64) AND MOD(CAST(`float64_col` AS INT64), 2) = 1
      THEN -1
      ELSE 1
    END
    ELSE POWER(
      `int64_col`,
      CASE
        WHEN ABS(`float64_col`) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(`float64_col`)
        ELSE `float64_col`
      END
    )
  END AS `int_pow_float`,
  CASE
    WHEN `int64_col` = CAST(0 AS INT64)
    THEN 1
    WHEN `float64_col` = 1
    THEN 1
    WHEN `float64_col` = CAST(0 AS INT64) AND `int64_col` < CAST(0 AS INT64)
    THEN CAST('Infinity' AS FLOAT64)
    WHEN ABS(`float64_col`) = CAST('Infinity' AS FLOAT64)
    THEN POWER(
      `float64_col`,
      CASE
        WHEN ABS(`int64_col`) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(`int64_col`)
        ELSE `int64_col`
      END
    )
    WHEN ABS(`int64_col`) > 9007199254740992
    THEN POWER(
      `float64_col`,
      CASE
        WHEN ABS(`int64_col`) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(`int64_col`)
        ELSE `int64_col`
      END
    )
    WHEN `float64_col` < CAST(0 AS INT64)
    AND NOT (
      CAST(`int64_col` AS INT64) = `int64_col`
    )
    THEN CAST('NaN' AS FLOAT64)
    WHEN `float64_col` <> CAST(0 AS INT64)
    AND `int64_col` * LN(ABS(`float64_col`)) > 709.78
    THEN CAST('Infinity' AS FLOAT64) * CASE
      WHEN `float64_col` < CAST(0 AS INT64) AND MOD(CAST(`int64_col` AS INT64), 2) = 1
      THEN -1
      ELSE 1
    END
    ELSE POWER(
      `float64_col`,
      CASE
        WHEN ABS(`int64_col`) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(`int64_col`)
        ELSE `int64_col`
      END
    )
  END AS `float_pow_int`,
  CASE
    WHEN `float64_col` = CAST(0 AS INT64)
    THEN 1
    WHEN `float64_col` = 1
    THEN 1
    WHEN `float64_col` = CAST(0 AS INT64) AND `float64_col` < CAST(0 AS INT64)
    THEN CAST('Infinity' AS FLOAT64)
    WHEN ABS(`float64_col`) = CAST('Infinity' AS FLOAT64)
    THEN POWER(
      `float64_col`,
      CASE
        WHEN ABS(`float64_col`) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(`float64_col`)
        ELSE `float64_col`
      END
    )
    WHEN ABS(`float64_col`) > 9007199254740992
    THEN POWER(
      `float64_col`,
      CASE
        WHEN ABS(`float64_col`) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(`float64_col`)
        ELSE `float64_col`
      END
    )
    WHEN `float64_col` < CAST(0 AS INT64)
    AND NOT (
      CAST(`float64_col` AS INT64) = `float64_col`
    )
    THEN CAST('NaN' AS FLOAT64)
    WHEN `float64_col` <> CAST(0 AS INT64)
    AND `float64_col` * LN(ABS(`float64_col`)) > 709.78
    THEN CAST('Infinity' AS FLOAT64) * CASE
      WHEN `float64_col` < CAST(0 AS INT64) AND MOD(CAST(`float64_col` AS INT64), 2) = 1
      THEN -1
      ELSE 1
    END
    ELSE POWER(
      `float64_col`,
      CASE
        WHEN ABS(`float64_col`) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(`float64_col`)
        ELSE `float64_col`
      END
    )
  END AS `float_pow_float`,
  CASE
    WHEN `int64_col` <> 0 AND 0 * LN(ABS(`int64_col`)) > 43.66827237527655
    THEN NULL
    ELSE CAST(POWER(CAST(`int64_col` AS NUMERIC), 0) AS INT64)
  END AS `int_pow_0`,
  CASE
    WHEN 0 = CAST(0 AS INT64)
    THEN 1
    WHEN `float64_col` = 1
    THEN 1
    WHEN `float64_col` = CAST(0 AS INT64) AND 0 < CAST(0 AS INT64)
    THEN CAST('Infinity' AS FLOAT64)
    WHEN ABS(`float64_col`) = CAST('Infinity' AS FLOAT64)
    THEN POWER(
      `float64_col`,
      CASE
        WHEN ABS(0) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(0)
        ELSE 0
      END
    )
    WHEN ABS(0) > 9007199254740992
    THEN POWER(
      `float64_col`,
      CASE
        WHEN ABS(0) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(0)
        ELSE 0
      END
    )
    WHEN `float64_col` < CAST(0 AS INT64) AND NOT (
      CAST(0 AS INT64) = 0
    )
    THEN CAST('NaN' AS FLOAT64)
    WHEN `float64_col` <> CAST(0 AS INT64) AND 0 * LN(ABS(`float64_col`)) > 709.78
    THEN CAST('Infinity' AS FLOAT64) * CASE
      WHEN `float64_col` < CAST(0 AS INT64) AND MOD(CAST(0 AS INT64), 2) = 1
      THEN -1
      ELSE 1
    END
    ELSE POWER(
      `float64_col`,
      CASE
        WHEN ABS(0) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(0)
        ELSE 0
      END
    )
  END AS `float_pow_0`,
  CASE
    WHEN `int64_col` <> 0 AND 1 * LN(ABS(`int64_col`)) > 43.66827237527655
    THEN NULL
    ELSE CAST(POWER(CAST(`int64_col` AS NUMERIC), 1) AS INT64)
  END AS `int_pow_1`,
  CASE
    WHEN 1 = CAST(0 AS INT64)
    THEN 1
    WHEN `float64_col` = 1
    THEN 1
    WHEN `float64_col` = CAST(0 AS INT64) AND 1 < CAST(0 AS INT64)
    THEN CAST('Infinity' AS FLOAT64)
    WHEN ABS(`float64_col`) = CAST('Infinity' AS FLOAT64)
    THEN POWER(
      `float64_col`,
      CASE
        WHEN ABS(1) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(1)
        ELSE 1
      END
    )
    WHEN ABS(1) > 9007199254740992
    THEN POWER(
      `float64_col`,
      CASE
        WHEN ABS(1) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(1)
        ELSE 1
      END
    )
    WHEN `float64_col` < CAST(0 AS INT64) AND NOT (
      CAST(1 AS INT64) = 1
    )
    THEN CAST('NaN' AS FLOAT64)
    WHEN `float64_col` <> CAST(0 AS INT64) AND 1 * LN(ABS(`float64_col`)) > 709.78
    THEN CAST('Infinity' AS FLOAT64) * CASE
      WHEN `float64_col` < CAST(0 AS INT64) AND MOD(CAST(1 AS INT64), 2) = 1
      THEN -1
      ELSE 1
    END
    ELSE POWER(
      `float64_col`,
      CASE
        WHEN ABS(1) > 9007199254740992
        THEN CAST('Infinity' AS FLOAT64) * SIGN(1)
        ELSE 1
      END
    )
  END AS `float_pow_1`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`