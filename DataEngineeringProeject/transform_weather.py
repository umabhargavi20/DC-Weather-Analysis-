import s3fs
from s3fs.core import S3FileSystem
import numpy as np
import pickle
import pandas as pd


def transform_data():
    s3 = S3FileSystem()
    # S3 bucket directory (data lake)
    DIR = 's3://ece5984-s3-umabhargavi/DataEngineeringProject/data_Lake'
    # Get data from S3 bucket as a pickle file
    raw_data = pd.read_pickle(s3.open('{}/{}'.format(DIR, 'Weather_data.pkl')))

    # Convert datetime and create year column
    raw_data['datetime'] = pd.to_datetime(raw_data['datetime'], format='%m/%d/%Y')
    raw_data['year'] = raw_data['datetime'].dt.year

    # Get unique years
    years = raw_data['year'].unique()

    # Save data by year
    for year in years:
        year_data = raw_data[raw_data['year'] == year]

        DIR_wh = 's3://ece5984-s3-umabhargavi/DataEngineeringProject/data_warehouse/'
        with s3.open('{}/{}'.format(DIR_wh, '{}.pkl'.format(year)), 'wb') as f:
            f.write(pickle.dumps(year_data))