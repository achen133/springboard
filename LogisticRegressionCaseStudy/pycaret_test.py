import pandas as pd
from pycaret.classification import *

df = pd.read_excel('./data/heart.xlsx', engine='openpyxl')
cats_ = ['sex_M_F', 'chest_pain_value', 'ECG_value', 'ST_slope_peak', 'defect_diag']

ex = setup(df, target='heart_disease', categorical_features=cats_)
print(ex)
