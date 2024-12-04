import s3fs
from s3fs.core import S3FileSystem
import numpy as np
import pickle
import pandas as pd
from pandas_datareader import data as pdr

def ingest_data():
    # Load the movie dataset from the current directory
    data = pd.read_csv('s3://ece5984-s3-umabhargavi/DataEngineeringProject/weather_data.csv')
    s3 = S3FileSystem()
    # S3 bucket directory
    DIR = 's3://ece5984-s3-umabhargavi/DataEngineeringProject/data_Lake'  # insert your S3 URI here
    # Push data to S3 bucket as a pickle file
    with s3.open('{}/{}'.format(DIR, 'Weather_data.pkl'), 'wb') as f:
        f.write(pickle.dumps(data))