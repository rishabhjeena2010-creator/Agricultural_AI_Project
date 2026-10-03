import requests
from datetime import date, timedelta

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

SEASON_PERIODS = {
    "Kharif": {
        "start_month": 6,
        "start_day": 1,
        "end_month": 10,
        "end_day": 31
    },
    "Rabi": {
        "start_month": 11,
        "start_day": 1,
        "end_month": 3,
        "end_day": 31
    },
    "Zaid": {
        "start_month": 3,
        "start_day": 1,
        "end_month": 6,
        "end_day": 30
    }
}


def get_location(location):
    params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(
        GEOCODING_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        raise ValueError(
            f"Location not found: {location}"
        )

    result = data["results"][0]

    return {
        "name": result.get("name"),
        "state": result.get("admin1"),
        "country": result.get("country"),
        "latitude": result.get("latitude"),
        "longitude": result.get("longitude")
    }


def get_season_dates(season):
    if season not in SEASON_PERIODS:
        raise ValueError(
            f"Invalid season: {season}"
        )

    today = date.today()
    current_year = today.year

    if season == "Rabi":
        start_date = date(
            current_year - 1,
            11,
            1
        )
        end_date = date(
            current_year,
            3,
            31
        )

    else:
        period = SEASON_PERIODS[season]

        start_date = date(
            current_year,
            period["start_month"],
            period["start_day"]
        )

        end_date = date(
            current_year,
            period["end_month"],
            period["end_day"]
        )

    return start_date, end_date


def get_weather(latitude, longitude, season):
    start_date, end_date = get_season_dates(season)

    today = date.today()

    if end_date >= today:
        end_date = today - timedelta(days=1)

    if start_date > end_date:
        raise ValueError(
            "Weather data is not available for the selected season yet."
        )

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": ",".join([
            "temperature_2m_mean",
            "precipitation_sum",
            "relative_humidity_2m_mean"
        ]),
        "timezone": "auto"
    }

    response = requests.get(
        ARCHIVE_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    return response.json()


def calculate_weather_summary(weather_data):
    daily = weather_data["daily"]

    temperatures = [
        value
        for value in daily["temperature_2m_mean"]
        if value is not None
    ]

    rainfall = [
        value
        for value in daily["precipitation_sum"]
        if value is not None
    ]

    humidity = [
        value
        for value in daily["relative_humidity_2m_mean"]
        if value is not None
    ]

    average_temperature = (
        sum(temperatures) / len(temperatures)
        if temperatures
        else 0
    )

    total_rainfall = sum(rainfall)

    average_humidity = (
        sum(humidity) / len(humidity)
        if humidity
        else 0
    )

    return {
        "average_temperature": round(
            average_temperature,
            2
        ),
        "total_rainfall": round(
            total_rainfall,
            2
        ),
        "average_humidity": round(
            average_humidity,
            2
        ),
        "number_of_days": len(
            daily["time"]
        )
    }


if __name__ == "__main__":
    location = get_location(
        "Gurugram, Haryana"
    )

    print("\n========== LOCATION ==========")
    print("Location:", location["name"])
    print("State:", location["state"])
    print("Country:", location["country"])
    print(
        "Coordinates:",
        location["latitude"],
        location["longitude"]
    )

    for season in ["Kharif", "Rabi", "Zaid"]:
        print(
            f"\n========== {season.upper()} WEATHER =========="
        )

        weather = get_weather(
            location["latitude"],
            location["longitude"],
            season
        )

        summary = calculate_weather_summary(
            weather
        )

        print(
            "Average Temperature:",
            summary["average_temperature"],
            "°C"
        )

        print(
            "Total Rainfall:",
            summary["total_rainfall"],
            "mm"
        )

        print(
            "Average Humidity:",
            summary["average_humidity"],
            "%"
        )

        print(
            "Days Analyzed:",
            summary["number_of_days"]
        )