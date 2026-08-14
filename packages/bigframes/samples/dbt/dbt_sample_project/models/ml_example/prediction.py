# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This DBT Python model prepares and trains a machine learning model to predict
# ozone levels.
#   1. Data Preparation: The model first gets a prepared dataset and splits it
#      into three subsets based on the year: training data (before 2017),
#      testing data (2017-2019), and prediction data (2020 and later).
#   2. Model Training: It then uses the LinearRegression model from BigFrames
#      ML library. The model is trained on the historical data, using other
#      atmospheric parameters to predict the 'o3' (ozone) levels.
#   3. Prediction: Finally, the trained model makes predictions on the most
#      recent data (from 2020 onwards) and returns the resulting DataFrame of
#      predicted ozone values.
#
# See more details from the related blog post: https://docs.getdbt.com/blog/train-linear-dbt-bigframes


def model(dbt, session):
    dbt.config(submission_method="bigframes", timeout=6000)

    df = dbt.ref("prepare_table")

    # Define the rules for separating the training, test and prediction data.
    train_data_filter = (df.date_local.dt.year < 2017)
    test_data_filter = (
        (df.date_local.dt.year >= 2017) & (df.date_local.dt.year < 2020)
    )
    predict_data_filter = (df.date_local.dt.year >= 2020)

    # Define index_columns again here in prediction.
    index_columns = ["state_name", "county_name", "site_num", "date_local", "time_local"]

    # Separate the training, test and prediction data.
    df_train = df[train_data_filter].set_index(index_columns)
    df_test = df[test_data_filter].set_index(index_columns)
    df_predict = df[predict_data_filter].set_index(index_columns)

    # Finalize the training dataframe.
    X_train = df_train.drop(columns="o3")
    y_train = df_train["o3"]

    # Finalize the prediction dataframe. 
    X_predict = df_predict.drop(columns="o3")

    # Import the LinearRegression model from bigframes.ml module.
    from bigframes.ml.linear_model import LinearRegression

    # Train the model.
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make the prediction using the model.
    df_pred = model.predict(X_predict)

    return df_pred
