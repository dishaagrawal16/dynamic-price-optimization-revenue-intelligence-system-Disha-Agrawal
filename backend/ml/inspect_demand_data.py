import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

file_path = os.path.join(DATA_DIR, "encoded_dataset.csv")

print("Looking for file at:")
print(os.path.abspath(file_path))

if not os.path.exists(file_path):
    print("\n❌ encoded_dataset.csv was NOT found.")
    print("\nFiles currently available in backend/data:")
    print(os.listdir(DATA_DIR))
    exit()

df = pd.read_csv(file_path)

print("\n===== ENCODED DATASET INFO =====")

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)