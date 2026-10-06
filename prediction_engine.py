from model import predict_yield
from weather import (
    get_location,
    get_weather,
    calculate_weather_summary,
    get_season_dates
)
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

    # ========================================================
    # ML YIELD PREDICTION
    # ========================================================

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


    # ========================================================
    # CALCULATE TOTAL ESTIMATED CROP
    # ========================================================

    total_yield = predicted_yield * area_hectares


    # ========================================================
    # WEATHER LOCATION
    # ========================================================

    location = f"{district}, {state}"

    location_data = get_location(location)


    # ========================================================
    # GET WEATHER DATA
    # ========================================================

    weather = get_weather(
        location_data["latitude"],
        location_data["longitude"],
        season
    )


    # ========================================================
    # WEATHER SUMMARY
    # ========================================================

    weather_summary = calculate_weather_summary(
        weather
    )


    # ========================================================
    # WEATHER SUITABILITY
    # ========================================================

    suitability = check_suitability(
        crop_type,
        weather_summary
    )


    # ========================================================
    # SEASON DATES
    # ========================================================

    start_date, end_date = get_season_dates(
        season
    )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {

        # Original ML prediction in kg/ha
        "predicted_yield": predicted_yield,

        # Total estimated crop for entered farm area in kg
        "total_yield": round(total_yield, 2),

        "location": location_data["name"],

        "state": location_data["state"],

        "country": location_data["country"],

        "season": season,

        "start_date": start_date,

        "end_date": end_date,

        "average_temperature":
            weather_summary["average_temperature"],

        "total_rainfall":
            weather_summary["total_rainfall"],

        "average_humidity":
            weather_summary["average_humidity"],

        "days_analyzed":
            weather_summary["number_of_days"],

        "temperature_status":
            suitability["temperature_status"],

        "rainfall_status":
            suitability["rainfall_status"],

        "humidity_status":
            suitability["humidity_status"],

        "overall_suitability":
            suitability["overall_status"]
    }
