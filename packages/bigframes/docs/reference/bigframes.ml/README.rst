BigQuery DataFrames ML
======================

As BigQuery DataFrames implements the Pandas API over top of BigQuery, BigQuery
DataFrame ML implements the SKLearn API over top of BigQuery Machine Learning.

Tutorial
--------

Start a session and initialize a dataframe for a BigQuery table

.. code-block:: python

    import bigframes.pandas

    df = bigframes.pandas.read_gbq("bigquery-public-data.ml_datasets.penguins")
    df

Clean and prepare the data

.. code-block:: python

    # filter down to the data we want to analyze
    adelie_data = df[df.species == "Adelie Penguin (Pygoscelis adeliae)"]

    # drop the columns we don't care about
    adelie_data = adelie_data.drop(columns=["species"])

    # drop rows with nulls to get our training data
    training_data = adelie_data.dropna()

    # take a peek at the training data
    training_data

.. code-block:: python

    # pick feature columns and label column
    X = training_data[['island', 'culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'sex']]
    y = training_data[['body_mass_g']]

Use train_test_split to create train and test datasets

.. code-block:: python

    from bigframes.ml.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2)

Define the model training pipeline

.. code-block:: python

    from bigframes.ml.linear_model import LinearRegression
    from bigframes.ml.pipeline import Pipeline
    from bigframes.ml.compose import ColumnTransformer
    from bigframes.ml.preprocessing import StandardScaler, OneHotEncoder

    preprocessing = ColumnTransformer([
        ("onehot", OneHotEncoder(), ["island", "species", "sex"]),
        ("scaler", StandardScaler(), ["culmen_depth_mm", "culmen_length_mm", "flipper_length_mm"]),
    ])

    model = LinearRegression(fit_intercept=False)

    pipeline = Pipeline([
        ('preproc', preprocessing),
        ('linreg', model)
    ])

    # view the pipeline
    pipeline

Train the pipeline

.. code-block:: python

    pipeline.fit(X_train, y_train)

Evaluate the model's performance on the test data

.. code-block:: python

    from bigframes.ml.metrics import r2_score

    y_pred = pipeline.predict(X_test)

    r2_score(y_test, y_pred)

Make predictions on new data

.. code-block:: python

    import pandas

    new_penguins = bigframes.pandas.read_pandas(
        pandas.DataFrame(
            {
                "tag_number": [1633, 1672, 1690],
                "species": [
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Adelie Penguin (Pygoscelis adeliae)",
                ],
                "island": ["Torgersen", "Torgersen", "Dream"],
                "culmen_length_mm": [39.5, 38.5, 37.9],
                "culmen_depth_mm": [18.8, 17.2, 18.1],
                "flipper_length_mm": [196.0, 181.0, 188.0],
                "sex": ["MALE", "FEMALE", "FEMALE"],
            }
        ).set_index("tag_number")
    )

    # view the new data
    new_penguins

.. code-block:: python

    pipeline.predict(new_penguins)

Save the trained model to BigQuery, so we can load it later

.. code-block:: python

    pipeline.to_gbq("bqml_tutorial.penguins_model", replace=True)
