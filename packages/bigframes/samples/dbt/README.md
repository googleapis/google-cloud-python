# dbt BigFrames Integration

This repository provides simple examples of using **dbt Python models** with **BigQuery** in **BigFrames** mode.

It includes basic configurations and sample models to help you get started quickly in a typical dbt project.

## Highlights

- `profiles.yml`: configures your connection to BigQuery.
- `dbt_project.yml`: configures your dbt project - **dbt_sample_project**.
- `dbt_bigframes_code_sample_1.py`: An example to read BigQuery data and perform basic transformation.
- `dbt_bigframes_code_sample_2.py`: An example to build an incremental model that leverages BigFrames UDF capabilities.
- `prepare_table.py`: An ML example to consolidate various data sources into a single, unified table for later usage.
- `prediction.py`: An ML example to train models and then generate predictions using the prepared table.

## Requirements

Before using this project, ensure you have:

- A [Google Cloud account](https://cloud.google.com/free?hl=en)
- A [dbt Cloud account](https://www.getdbt.com/signup) (if using dbt Cloud)
- Python and SQL basics
- Familiarity with dbt concepts and structure

For more, see:
- https://docs.getdbt.com/guides/dbt-python-bigframes
- https://cloud.google.com/bigquery/docs/dataframes-dbt

## Run Locally

Follow these steps to run the Python models using dbt Core.

1. **Install the dbt BigQuery adapter:**

    ```bash
    pip install dbt-bigquery
    ```

2. **Initialize a dbt project (if not already done):**

    ```bash
    dbt init
    ```

    Follow the prompts to complete setup.

3. **Finish the configuration and add sample code:**

    - Edit `~/.dbt/profiles.yml` to finish the configuration.
    - Replace or add code samples in `.../models/example`.

4. **Run your dbt models:**

    To run all models:

    ```bash
    dbt run
    ```

    Or run a specific model:

    ```bash
    dbt run --select your_model_name
    ```