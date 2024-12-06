import s3fs
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import TimeSeriesSplit
import pickle

def feature_extract():
    s3 = s3fs.S3FileSystem()
    DIR = 's3://ece5984-s3-umabhargavi/DataEngineeringProject/data_warehouse//'  # S3 directory for weather data
    weather_data = []

    # Load yearly data
    for year in range(2015, 2025):
        file_path = f"{DIR}{year}.pkl"
        with s3.open(file_path, 'rb') as f:
            yearly_data = pd.read_pickle(f)
            weather_data.append(yearly_data)

    combined_data = pd.concat(weather_data, ignore_index=True)

    # Select features and target
    features = ['tempmax', 'tempmin', 'humidity', 'precip', 'windgust','year']

    target = 'temp'

    # Scale features
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(combined_data[features])

    # Split data into training and testing sets
    timesplit = TimeSeriesSplit(n_splits=5)
    for train_index, test_index in timesplit.split(scaled_features):
        X_train, X_test = scaled_features[train_index], scaled_features[test_index]
        y_train, y_test = combined_data[target].iloc[train_index], combined_data[target].iloc[test_index]

    # Save to S3
    DIR_wh = 's3://ece5984-s3-umabhargavi/DataEngineeringProject/feature_extraction/'
    with s3.open(f'{DIR_wh}X_train.pkl', 'wb') as f:
        pickle.dump(X_train, f)
    with s3.open(f'{DIR_wh}X_test.pkl', 'wb') as f:
        pickle.dump(X_test, f)
    with s3.open(f'{DIR_wh}y_train.pkl', 'wb') as f:
        pickle.dump(y_train, f)
    with s3.open(f'{DIR_wh}y_test.pkl', 'wb') as f:
        pickle.dump(y_test, f)
