import pandas as pd
from model import predict_yield

CSV_PATH = "data/agricultural_harvest_yield_1500_final.csv"

df = pd.read_csv(CSV_PATH)

df["Sowing_Date"] = pd.to_datetime(
    df["Sowing_Date"],
    origin="1899-12-30",
    unit="D"
)

df["Sowing_Month"] = df["Sowing_Date"].dt.month

test_input = {
    "State": "Haryana",
    "District": "Gurugram",
    "Crop_Year": 2023,
    "Crop_Type": "Maize",
    "Season": "Kharif",
    "Area_Hectares": 2.7,
    "Fertilizer_Type": "NPK",
    "Fertilizer_Amount_kg_ha": 135,
    "Irrigation_Method": "Drip",
    "Irrigation_Frequency": 6,
    "Pesticide_Used": "Yes",
    "Pest_Infection_Level": "Low",
    "Sowing_Month": 7
}

features = list(test_input.keys())

existing_rows = df[
    (df[features] == pd.Series(test_input)).all(axis=1)
]

print("\n========== TEST INPUT ==========")

for feature, value in test_input.items():
    print(f"{feature}: {value}")

print("\n========== DATASET CHECK ==========")

if len(existing_rows) > 0:
    print("WARNING: This exact input already exists in the dataset.")
    print("Prediction test stopped.")

else:
    print("This exact input does NOT exist in the dataset.")
    print("Safe to use as a new manual test.")

    predicted_yield = predict_yield(
        state=test_input["State"],
        district=test_input["District"],
        crop_year=test_input["Crop_Year"],
        crop_type=test_input["Crop_Type"],
        season=test_input["Season"],
        area_hectares=test_input["Area_Hectares"],
        fertilizer_type=test_input["Fertilizer_Type"],
        fertilizer_amount=test_input["Fertilizer_Amount_kg_ha"],
        irrigation_method=test_input["Irrigation_Method"],
        irrigation_frequency=test_input["Irrigation_Frequency"],
        pesticide_used=test_input["Pesticide_Used"],
        pest_infection_level=test_input["Pest_Infection_Level"],
        sowing_month=test_input["Sowing_Month"]
    )

    print("\n========== YIELD PREDICTION ==========")
    print("Predicted Yield:", predicted_yield, "kg/ha")