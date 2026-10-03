import pandas as pd

# -----------------------------------
# LOAD DATASET
# -----------------------------------

file_path = "data/agricultural_harvest_yield_1500_final.csv"

df = pd.read_csv(file_path)


# -----------------------------------
# BASIC INFORMATION
# -----------------------------------

print("\n========== DATASET SHAPE ==========")
print(df.shape)


print("\n========== COLUMN NAMES ==========")

for i, column in enumerate(df.columns, start=1):
    print(i, column)


print("\n========== DATA TYPES ==========")
print(df.dtypes)


# -----------------------------------
# MISSING VALUES
# -----------------------------------

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())


# -----------------------------------
# DUPLICATE ROWS
# -----------------------------------

print("\n========== DUPLICATE ROWS ==========")
print(df.duplicated().sum())


# -----------------------------------
# CROP TYPES
# -----------------------------------

print("\n========== CROP TYPES ==========")
print(df["Crop_Type"].value_counts())


# -----------------------------------
# TARGET VARIABLE
# -----------------------------------

print("\n========== YIELD STATISTICS ==========")
print(df["Yield_kg_ha"].describe())


# -----------------------------------
# YIELD BY CROP
# -----------------------------------

print("\n========== YIELD BY CROP ==========")

yield_by_crop = df.groupby("Crop_Type")["Yield_kg_ha"].agg(
    ["count", "min", "max", "mean"]
)

print(yield_by_crop.sort_values("mean", ascending=False))


# -----------------------------------
# FIRST 5 RECORDS
# -----------------------------------

print("\n========== FIRST 5 RECORDS ==========")
print(df.head())