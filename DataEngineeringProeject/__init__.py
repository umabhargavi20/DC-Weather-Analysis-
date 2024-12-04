print('hello pythin')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import *
movie_df = pd.read_excel('C:\\Users\\umaat\\PycharmProjects\\DataEngineering\\pythonProject1\\weather_data.xlsx')

# Displaying the first 10 records
print(movie_df.head(10))
print(movie_df.info())


