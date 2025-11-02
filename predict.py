import joblib
import pandas as pd
import numpy as np
from train import columns
from typing import List

saved_model = joblib.load('model.joblib')

def make_prediction(data: dict) -> float:
    data = pd.DataFrame(data=[data.values()], columns=columns)
    return saved_model.predict(data)[0]

def make_batch_prediction(data: List[dict]) -> np.array:
    X = pd.DataFrame(data=[x.values() for x in data], columns=columns)
    return saved_model.predict(X)