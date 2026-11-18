import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
import joblib
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join(BASE_DIR, "..", "data", "cleaned_dataset.csv")

df = pd.read_csv(input_path)

category_encoder = LabelEncoder()
payment_encoder = LabelEncoder()
weekday_encoder = LabelEncoder()

df["Category"] = category_encoder.fit_transform(df["Category"])
df["Payment_Method"] = payment_encoder.fit_transform(df["Payment_Method"])
df["Weekday"] = weekday_encoder.fit_transform(df["Weekday"])
print("Category Mapping:")
for i, label in enumerate(category_encoder.classes_):
    print(f"{label} -> {i}")

print("\nPayment Method Mapping:")
for i, label in enumerate(payment_encoder.classes_):
    print(f"{label} -> {i}")

print("\nWeekday Mapping:")
for i, label in enumerate(weekday_encoder.classes_):
    print(f"{label} -> {i}")

output_path = os.path.join(BASE_DIR, "..", "data", "encoded_dataset.csv")
df.to_csv(output_path, index=False)

print(output_path)
joblib.dump(category_encoder, os.path.join(BASE_DIR, "category_encoder.pkl"))
joblib.dump(payment_encoder, os.path.join(BASE_DIR, "payment_encoder.pkl"))
joblib.dump(weekday_encoder, os.path.join(BASE_DIR, "weekday_encoder.pkl"))

print("\n✅ Encoders saved successfully!")