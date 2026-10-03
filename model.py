import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model",
    "agricultural_yield_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_yield(
    state,
    district,
    crop_year,
    crop_type,
    season,
    area_hectares,
    fertilizer_type,
    fertilizer_amount,
    irrigation_method,
    irrigation_frequency,
    pesticide_used,
    pest_infection_level,
    sowing_month
):
    input_data = pd.DataFrame([{
        "State": state,
        "District": district,
        "Crop_Year": crop_year,
        "Crop_Type": crop_type,
        "Season": season,
        "Area_Hectares": area_hectares,
        "Fertilizer_Type": fertilizer_type,
        "Fertilizer_Amount_kg_ha": fertilizer_amount,
        "Irrigation_Method": irrigation_method,
        "Irrigation_Frequency": irrigation_frequency,
        "Pesticide_Used": pesticide_used,
        "Pest_Infection_Level": pest_infection_level,
        "Sowing_Month": sowing_month
    }])

    prediction = model.predict(input_data)[0]

    return round(prediction, 2)


if __name__ == "__main__":

    predicted_yield = predict_yield(
        state="Haryana",
        district="Gurugram",
        crop_year=2022,
        crop_type="Maize",
        season="Kharif",
        area_hectares=2.5,
        fertilizer_type="NPK",
        fertilizer_amount=120,
        irrigation_method="Drip",
        irrigation_frequency=5,
        pesticide_used="Yes",
        pest_infection_level="Low",
        sowing_month=6
    )

    print("\n========== YIELD PREDICTION ==========")
    print("Predicted Yield:", predicted_yield, "kg/ha")