import os
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "..",
    "data"
)


# Decathlon data
decathlon_path = os.path.join(
    DATA_DIR,
    "competitor_prices.csv"
)

# Myntra + Nykaa data
multi_path = os.path.join(
    DATA_DIR,
    "competitor_prices_v2.csv"
)

# Crossword Books data
crossword_path = os.path.join(
    DATA_DIR,
    "competitor_books_crossword.csv"
)

# Croma Electronics data
croma_path = os.path.join(
    DATA_DIR,
    "competitor_croma.csv"
)

# Final combined file
output_path = os.path.join(
    DATA_DIR,
    "competitor_prices_final.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading Decathlon data...")

decathlon = pd.read_csv(
    decathlon_path
)

print(
    "Decathlon rows:",
    len(decathlon)
)


print("\nLoading Myntra + Nykaa data...")

multi = pd.read_csv(
    multi_path
)

print(
    "Myntra + Nykaa rows:",
    len(multi)
)


print("\nLoading Crossword data...")

crossword = pd.read_csv(
    crossword_path
)

print(
    "Crossword rows:",
    len(crossword)
)


print("\nLoading Croma data...")

croma = pd.read_csv(
    croma_path
)

print(
    "Croma rows:",
    len(croma)
)


# ============================================================
# STANDARDIZE COLUMNS
# ============================================================

columns = [
    "Category",
    "Subcategory",
    "Competitor",
    "Brand",
    "Product_Name",
    "Author",
    "Competitor_Price",
    "MRP",
    "Source",
    "Scraped_At"
]


# Make sure every dataset contains every column
datasets = [
    decathlon,
    multi,
    crossword,
    croma
]


for df in datasets:

    for col in columns:

        if col not in df.columns:
            df[col] = ""


# Keep only standard columns
decathlon = decathlon[columns]

multi = multi[columns]

crossword = crossword[columns]

croma = croma[columns]


# ============================================================
# COMBINE
# ============================================================

final_df = pd.concat(
    [
        decathlon,
        multi,
        crossword,
        croma
    ],
    ignore_index=True
)


# ============================================================
# CLEAN DATA TYPES
# ============================================================

final_df["Competitor_Price"] = pd.to_numeric(
    final_df["Competitor_Price"],
    errors="coerce"
)

final_df["MRP"] = pd.to_numeric(
    final_df["MRP"],
    errors="coerce"
)


# Remove rows without a valid competitor price
final_df = final_df.dropna(
    subset=["Competitor_Price"]
)


# ============================================================
# REMOVE DUPLICATES
# ============================================================

final_df = final_df.drop_duplicates(
    subset=[
        "Competitor",
        "Product_Name",
        "Competitor_Price"
    ]
)


# ============================================================
# SAVE
# ============================================================

final_df.to_csv(
    output_path,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\n========================================")
print("COMPETITOR DATA MERGED")
print("========================================")

print(
    "Total competitor products:",
    len(final_df)
)


print("\nProducts by category:")

print(
    final_df.groupby(
        [
            "Category",
            "Competitor"
        ]
    ).size()
)


print("\nPrice statistics:")

print(
    final_df.groupby(
        "Competitor"
    )["Competitor_Price"]
    .agg(
        [
            "count",
            "mean",
            "min",
            "max"
        ]
    )
    .round(2)
)


print("\nSaved at:")

print(
    os.path.abspath(
        output_path
    )
)