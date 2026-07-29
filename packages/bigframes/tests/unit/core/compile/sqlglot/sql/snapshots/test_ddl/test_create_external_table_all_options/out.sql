CREATE OR REPLACE EXTERNAL TABLE `my-project.my_dataset.my_table` (
  `col1` INT64,
  `col2` STRING
) WITH CONNECTION `my-connection` WITH PARTITION COLUMNS (
  `part1` DATE,
  `part2` STRING
) OPTIONS (
  format='CSV',
  uris=['gs://bucket/path*']
)