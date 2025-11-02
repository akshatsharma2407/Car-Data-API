import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

df = (
    pd.read_csv('C:/Users/aksha/OneDrive/Desktop/cars_mlops_practice/autonexus/data/raw/train.csv')
    .dropna()
    .drop(
        columns=
        ['Unnamed: 0','Unnamed: 0.1','Km/L','Km/L_e_City','Km/L_e_Hwy',
         'Valves','Engine_Size','Gear_Spec','Expected_Range','Battery_Capacity',
         'Dc_Fast_Charging','Level2_Charging','Personal_Use_Only'])
)

X = df.drop(columns='Price')
y = df['Price'].copy()

columns = X.columns

lr = LinearRegression().fit(X,y)

joblib.dump(lr, 'model.joblib')