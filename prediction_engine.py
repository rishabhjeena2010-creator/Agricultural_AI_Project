from model import predict_yield
from weather import get_location, get_weather, calculate_weather_summary, get_season_dates
from crop_requirements import check_suitability


def run_prediction(
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
    predicted_yield = predict_yield(
        state=state,
        district=district,
        crop_year=crop_year,
        crop_type=crop_type,
        season=season,
        area_hectares=area_hectares,
        fertilizer_type=fertilizer_type,
        fertilizer_amount=fertilizer_amount,
        irrigation_method=irrigation_method,
        irrigation_frequency=irrigation_frequency,
        pesticide_used=pesticide_used,
        pest_infection_level=pest_infection_level,
        sowing_month=sowing_month
    )

    location = f"{district}, {state}"

    location_data = get_location(location)

    weather = get_weather(
        location_data["latitude"],
        location_data["longitude"],
        season
    )

    weather_summary = calculate_weather_summary(weather)

    suitability = check_suitability(
        crop_type,
        weather_summary
    )

    start_date, end_date = get_season_dates(season)

    return {
        "predicted_yield": predicted_yield,
        "location": location_data["name"],
        "state": location_data["state"],
        "country": location_data["country"],
        "season": season,
        "start_date": start_date,
        "end_date": end_date,
        "average_temperature": weather_summary["average_temperature"],
        "total_rainfall": weather_summary["total_rainfall"],
        "average_humidity": weather_summary["average_humidity"],
        "days_analyzed": weather_summary["number_of_days"],
        "temperature_status": suitability["temperature_status"],
        "rainfall_status": suitability["rainfall_status"],
        "humidity_status": suitability["humidity_status"],
        "overall_suitability": suitability["overall_status"]
    }


if __name__ == "__main__":
    result = run_prediction(
        state="Haryana",
        district="Gurugram",
        crop_year=2026,
        crop_type="Maize",
        season="Kharif",
        area_hectares=2.7,
        fertilizer_type="NPK",
        fertilizer_amount=135,
        irrigation_method="Drip",
        irrigation_frequency=6,
        pesticide_used="Yes",
        pest_infection_level="Low",
        sowing_month=7
    )

    print("\n========== PREDICTION ==========")
    print("Predicted Yield:", result["predicted_yield"], "kg/ha")

    print("\n========== WEATHER ==========")
    print("Season:", result["season"])
    print("Average Temperature:", result["average_temperature"], "°C")
    print("Total Rainfall:", result["total_rainfall"], "mm")
    print("Average Humidity:", result["average_humidity"], "%")
    print("Days Analyzed:", result["days_analyzed"])

    print("\n========== SUITABILITY ==========")
    print("Temperature:", result["temperature_status"])
    print("Rainfall:", result["rainfall_status"])
    print("Humidity:", result["humidity_status"])
    print("Overall:", result["overall_suitability"])