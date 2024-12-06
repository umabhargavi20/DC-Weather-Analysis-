import s3fs
import numpy as np
import pickle
from sklearn.ensemble import GradientBoostingRegressor
import tempfile

def build_train():
    s3 = s3fs.S3FileSystem()
    # S3 bucket directory (data warehouse)
    DIR_weather = 's3://ece5984-s3-umabhargavi/DataEngineeringProject/feature_extraction/'  # Replace with your S3 directory

    # Load training and testing datasets from S3
    X_train = np.load(s3.open(f'{DIR_weather}X_train.pkl', 'rb'), allow_pickle=True)
    X_test = np.load(s3.open(f'{DIR_weather}X_test.pkl', 'rb'), allow_pickle=True)
    y_train = np.load(s3.open(f'{DIR_weather}y_train.pkl', 'rb'), allow_pickle=True)
    y_test = np.load(s3.open(f'{DIR_weather}y_test.pkl', 'rb'), allow_pickle=True)

    # Initialize Gradient Boosting Regressor
    gbr = GradientBoostingRegressor(
        n_estimators=100,  # Number of boosting stages
        learning_rate=0.1,  # Learning rate
        max_depth=3,  # Maximum depth of trees
        random_state=42
    )

    # Train the Gradient Boosting model
    gbr.fit(X_train, y_train)

    # Make predictions
    y_pred = gbr.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Store metrics in a dictionary
    metrics = {
        "Mean Squared Error (MSE)": mse,
        "Mean Absolute Error (MAE)": mae,
        "R2 Score": r2
    }

    # Save model and metrics temporarily, then upload to S3
    with tempfile.TemporaryDirectory() as tempdir:
        # Save the model
        model_path = f"{tempdir}/gradient_boosting_weather.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(gbr, f)
        s3.put(model_path, f"{DIR_weather}gradient_boosting_weather.pkl")

        # Save the metrics
        metrics_path = f"{tempdir}/gradient_boosting_metrics.pkl"
        with open(metrics_path, 'wb') as f:
            pickle.dump(metrics, f)
        s3.put(metrics_path, f"{DIR_weather}gradient_boosting_metrics.pkl")

