# Predicting Daily Weather Patterns in Washington DC

## Description

### Objective
This project forecasts daily weather metrics such as temperature, precipitation, and humidity using historical data from 2015-2024. Accurate predictions support decision-making in agriculture, energy planning, and public safety.

### Dataset
Sourced from Kaggle, the dataset spans nine years with 33 weather features. Preprocessing ensures quality, handling missing data and encoding categorical fields for machine learning.

### Tools & Technologies
Data Ingestion: Apache Airflow
Data Storage: S3 Bucket
Modeling: Machine Learning
Visualization: Tableau

### Pipeline / Architecture
We are utilizing the Washington DC Historical Weather dataset from Kaggle, which spans 2015-2024 and includes 33 weather features. Our project’s goal is to build a Batch-ML-Visualization pipeline for daily temperature forecasting in Washington, DC.

Data Ingestion: Data is batch-ingested using Apache Airflow, automating regular data pulls and storage in our S3 bucket.
Modeling: We plan to integrate machine learning steps for predicting temperature and, if possible, precipitation.
Visualization: The pipeline concludes with Tableau visualizations, enabling clear comparisons of predicted and observed weather patterns over time.

### Data Quality Assessment
The Washington DC Historical Weather dataset from Kaggle is of overall good quality, sourced from reliable weather stations and maintained by Visual Crossing. Initial inspections reveal that the data is consistent and aligns with expected weather patterns for Washington DC. However, certain fields require cleaning to handle missing or inconsistent values.
The dataset spans nine years (2015-2024) and contains 33 features. While most fields are fully populated, some fields, such as severerisk, have sparse data before 2022. These fields were excluded from the model due to insufficient coverage. The preciptype field contains blanks for days without precipitation. These blanks were converted to 0 (indicating no precipitation).
The dataset was consistent across features with no duplicate rows. Temporal patterns matched expected weather cycles. Columns like sunrise/sunset times and moon phases were removed as they were redundant or irrelevant for predictive purposes.
For the precipitation type field, which contains values such as rain, snow, and ice, we used one-hot encoding to create separate fields for each type. Each new field contains a value of 1 if the type was present and 0 if it was not.
After preprocessing, the dataset was found to be suitable for machine learning tasks. No further significant issues were detected that could impact modeling.

### Data Transformation Models used

For this project, we implemented a two-step process consisting of Feature Extraction and Data Modeling. In the Feature Extraction stage, we combined raw weather data segmented by year (2015–2024) from an S3 bucket into a single dataset. Key features such as **tempmax, tempmin, humidity, precip, windgust, and year** were selected, and the target variable, **temp**, was defined for prediction. The data was scaled using MinMaxScaler to normalize values between 0 and 1 for improved model performance. A TimeSeriesSplit was used to partition the data into training and testing sets, ensuring temporal order was preserved. The processed datasets were then saved back to S3 for use in subsequent steps.

In the Data Modeling stage, we utilized a **Gradient Boosting Regressor** due to its ability to handle non-linear relationships and perform well on smaller datasets. The model was configured with **100 boosting stages, a learning rate of 0.1, and a maximum tree depth of 3**. It was trained using the extracted features and evaluated on the test data. Evaluation metrics included **Mean Squared Error (MSE) to measure the average squared prediction error, Mean Absolute Error (MAE)** to quantify the average magnitude of errors, and **R² Score** to determine the variance explained by the model. Both the trained model and its evaluation metrics were serialized and stored in S3 for reproducibility and further analysis. This modular and scalable workflow ensures efficient processing, accurate predictions, and seamless integration into broader data pipelines

The evaluation of the Gradient Boosting model demonstrates its strong predictive performance on the weather dataset. The **Mean Squared Error (MSE) of 0.311** indicates that, on average, the squared differences between the predicted and actual values are minimal, showcasing the model's accuracy in capturing the underlying trends in the data. Similarly, the **Mean Absolute Error (MAE) of 0.413** suggests that the model's predictions deviate by an average of 0.413 units from the actual values, which is a small error given that the data is normalized. Furthermore, the model achieved an impressive **R² Score of 0.996**, signifying that it explains 99.6% of the variance in the target variable (temp). This high R² value reflects the model's ability to accurately learn the relationship between the input features (tempmax, tempmin, humidity, precip, windgust, and year) and the target variable. Overall, these results indicate that the Gradient Boosting model is highly effective for this weather prediction task, though further validation on unseen data is recommended to ensure its generalizability.


**Infographic:**
A simple infographic describing the architecture of your data pipeline including datasets, storage, and tools used along with another final infographic describing the results of the engineering task accomplished. Examples can be provided if needed.​​

