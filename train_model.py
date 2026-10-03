import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# 1. LOAD DATASET
# ============================================================

file_path = "data/agricultural_harvest_yield_1500_final.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully.")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 2. CONVERT DATES
# ============================================================

df["Sowing_Date"] = pd.to_datetime(
    df["Sowing_Date"],
    origin="1899-12-30",
    unit="D"
)

df["Harvest_Date"] = pd.to_datetime(
    df["Harvest_Date"],
    origin="1899-12-30",
    unit="D"
)

# Extract month from sowing date
df["Sowing_Month"] = df["Sowing_Date"].dt.month


# ============================================================
# 3. DEFINE TARGET
# ============================================================

target = "Yield_kg_ha"

X = df.drop(columns=[target])
y = df[target]


# ============================================================
# 4. REMOVE UNWANTED FEATURES
# ============================================================

columns_to_remove = [

    # ----------------------------
    # ID / date information
    # ----------------------------
    "Record_ID",
    "Sowing_Date",
    "Harvest_Date",

    # ----------------------------
    # WEATHER FEATURES
    # ----------------------------
    "Temperature_Avg_C",
    "Rainfall_mm",
    "Humidity_Percent",

    # ----------------------------
    # SOIL FEATURES
    # ----------------------------
    "Soil_Type",
    "Soil_pH",
    "Nitrogen_mg_kg",
    "Phosphorus_mg_kg",
    "Potassium_mg_kg",

    # ----------------------------
    # POST-HARVEST / TARGET LEAKAGE
    # ----------------------------
    "Growth_Duration_Days",
    "Production_kg",
    "Production_Cost_INR_ha",
    "Total_Cost_INR",
    "Market_Price_INR_kg",
    "Profit_INR"
]

X = X.drop(columns=columns_to_remove)


# ============================================================
# 5. DISPLAY FEATURES BEING USED
# ============================================================

print("\n========== FEATURES USED BY MODEL ==========")

for column in X.columns:
    print("-", column)


# ============================================================
# 6. IDENTIFY CATEGORICAL AND NUMERICAL FEATURES
# ============================================================

categorical_columns = X.select_dtypes(
    include=["object", "string"]
).columns.tolist()

numerical_columns = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()


print("\n========== CATEGORICAL FEATURES ==========")
print(categorical_columns)

print("\n========== NUMERICAL FEATURES ==========")
print(numerical_columns)


# ============================================================
# 7. PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[

        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        ),

        (
            "numerical",
            "passthrough",
            numerical_columns
        )
    ]
)


# ============================================================
# 8. RANDOM FOREST MODEL
# ============================================================

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)


# ============================================================
# 9. CREATE PIPELINE
# ============================================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ============================================================
# 10. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


print("\n========== DATA SPLIT ==========")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))


# ============================================================
# 11. TRAIN MODEL
# ============================================================

print("\nTraining Random Forest model...")

pipeline.fit(
    X_train,
    y_train
)

print("Training completed.")


# ============================================================
# 12. MAKE PREDICTIONS
# ============================================================

y_pred = pipeline.predict(X_test)


# ============================================================
# 13. MODEL PERFORMANCE
# ============================================================

mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred
    )
)

r2 = r2_score(
    y_test,
    y_pred
)


print("\n========== MODEL PERFORMANCE ==========")

print(f"MAE  : {mae:.2f} kg/ha")
print(f"RMSE : {rmse:.2f} kg/ha")
print(f"R²   : {r2:.4f}")


# ============================================================
# 14. FEATURE IMPORTANCE
# ============================================================

feature_names = (
    pipeline
    .named_steps["preprocessor"]
    .get_feature_names_out()
)

importances = (
    pipeline
    .named_steps["model"]
    .feature_importances_
)


feature_importance = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
})


feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)


print("\n========== TOP 20 IMPORTANT FEATURES ==========")

print(
    feature_importance
    .head(20)
    .to_string(index=False)
)


# ============================================================
# 15. SAVE FEATURE IMPORTANCE
# ============================================================

feature_importance.to_csv(
    "feature_importance.csv",
    index=False
)

print("\nFeature importance saved to:")
print("feature_importance.csv")


# ============================================================
# 16. SAVE TRAINED MODEL
# ============================================================

os.makedirs(
    "model",
    exist_ok=True
)

model_path = "model/agricultural_yield_model.pkl"

joblib.dump(
    pipeline,
    model_path
)

print("\nModel saved successfully:")
print(model_path)


# ============================================================
# 17. 5-FOLD CROSS-VALIDATION
# ============================================================

print("\n========== 5-FOLD CROSS-VALIDATION ==========")

cv_scores = cross_val_score(
    pipeline,
    X,
    y,
    cv=5,
    scoring="r2",
    n_jobs=-1
)


print("R² scores for each fold:")
print(cv_scores)

print(
    f"Mean R²: {cv_scores.mean():.4f}"
)

print(
    f"Standard Deviation: {cv_scores.std():.4f}"
)


# ============================================================
# 18. FINAL SUMMARY
# ============================================================

print("\n========== FINAL SUMMARY ==========")

print("Target:", target)
print("Total records:", len(df))
print("Features used:", len(X.columns))
print(f"Test MAE: {mae:.2f} kg/ha")
print(f"Test RMSE: {rmse:.2f} kg/ha")
print(f"Test R²: {r2:.4f}")
print(f"Cross-validation Mean R²: {cv_scores.mean():.4f}")

print("\nModel training completed successfully.")