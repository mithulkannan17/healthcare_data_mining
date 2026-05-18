import pandas as pd

DATASET_PATH = 'data/indian_diseases_dataset.csv'

def load_dataset():
    df = pd.read_csv(DATASET_PATH)
    return df

