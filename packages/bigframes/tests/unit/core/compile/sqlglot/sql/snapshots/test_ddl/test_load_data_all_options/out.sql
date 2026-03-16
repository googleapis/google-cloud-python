LOAD DATA OVERWRITE INTO `my-project.my_dataset.my_table` (
  `col1` INT64,
  `col2` STRING
) PARTITION BY `date_col` CLUSTER BY
  `cluster_col` OPTIONS (
  description='my table'
) FROM FILES (format='CSV', uris=['gs://bucket/path*']) WITH PARTITION COLUMNS (
  `part1` DATE,
  `part2` STRING
) WITH CONNECTION `my-connection`