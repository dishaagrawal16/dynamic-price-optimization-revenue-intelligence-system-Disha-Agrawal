import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "ecommerce_dataset_updated.csv"
)


df = pd.read_csv(csv_path)

print("Original Shape:", df.shape)


df.drop_duplicates(inplace=True)

df.dropna(inplace=True)


df["Purchase_Date"] = pd.to_datetime(
    df["Purchase_Date"],
    dayfirst=True
)

df["Year"] = df["Purchase_Date"].dt.year
df["Month"] = df["Purchase_Date"].dt.month
df["Day"] = df["Purchase_Date"].dt.day
df["Weekday"] = df["Purchase_Date"].dt.day_name()

print("Cleaned Shape:", df.shape)

output_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "cleaned_dataset.csv"
)

df.to_csv(output_path, index=False)

print("Dataset cleaned successfully!")
print("Saved at:", output_path)