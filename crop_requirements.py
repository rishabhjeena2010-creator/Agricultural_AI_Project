# ============================================================
# CROP WEATHER REQUIREMENTS
# ============================================================

CROP_REQUIREMENTS = {

    "Maize": {
        "temperature": (18, 32),
        "rainfall": (450, 750),
        "humidity": (50, 80)
    },

    "Rice": {
        "temperature": (20, 35),
        "rainfall": (1000, 2000),
        "humidity": (70, 90)
    },

    "Wheat": {
        "temperature": (10, 25),
        "rainfall": (300, 600),
        "humidity": (40, 70)
    },

    "Cotton": {
        "temperature": (21, 35),
        "rainfall": (500, 1000),
        "humidity": (50, 80)
    },

    "Mustard": {
        "temperature": (10, 25),
        "rainfall": (250, 500),
        "humidity": (40, 70)
    },

    "Groundnut": {
        "temperature": (21, 30),
        "rainfall": (500, 1000),
        "humidity": (50, 75)
    },

    "Soybean": {
        "temperature": (20, 30),
        "rainfall": (450, 700),
        "humidity": (60, 80)
    },

    "Bajra": {
        "temperature": (25, 35),
        "rainfall": (300, 600),
        "humidity": (40, 70)
    },

    "Jowar": {
        "temperature": (25, 32),
        "rainfall": (400, 750),
        "humidity": (40, 70)
    },

    "Barley": {
        "temperature": (12, 25),
        "rainfall": (300, 500),
        "humidity": (40, 70)
    },

    "Moong": {
        "temperature": (25, 35),
        "rainfall": (350, 600),
        "humidity": (50, 75)
    }
}


# ============================================================
# GET REQUIREMENTS FOR A CROP
# ============================================================

def get_crop_requirements(crop):

    if crop not in CROP_REQUIREMENTS:
        raise ValueError(
            f"No weather requirements available for {crop}"
        )

    return CROP_REQUIREMENTS[crop]


# ============================================================
# CHECK WEATHER SUITABILITY
# ============================================================

def check_suitability(crop, weather):

    requirements = get_crop_requirements(crop)

    temperature = weather["average_temperature"]
    rainfall = weather["total_rainfall"]
    humidity = weather["average_humidity"]

    temp_min, temp_max = requirements["temperature"]
    rain_min, rain_max = requirements["rainfall"]
    humidity_min, humidity_max = requirements["humidity"]

    temperature_ok = temp_min <= temperature <= temp_max
    rainfall_ok = rain_min <= rainfall <= rain_max
    humidity_ok = humidity_min <= humidity <= humidity_max

    if temperature_ok:
        temperature_status = "Suitable"
    else:
        temperature_status = "Outside preferred range"

    if rainfall_ok:
        rainfall_status = "Suitable"
    else:
        rainfall_status = "Outside preferred range"

    if humidity_ok:
        humidity_status = "Suitable"
    else:
        humidity_status = "Outside preferred range"

    suitable_count = sum([
        temperature_ok,
        rainfall_ok,
        humidity_ok
    ])

    if suitable_count == 3:
        overall_status = "Suitable"

    elif suitable_count == 2:
        overall_status = "Partially Suitable"

    else:
        overall_status = "Less Suitable"

    return {
        "temperature": temperature,
        "temperature_range": requirements["temperature"],
        "temperature_status": temperature_status,

        "rainfall": rainfall,
        "rainfall_range": requirements["rainfall"],
        "rainfall_status": rainfall_status,

        "humidity": humidity,
        "humidity_range": requirements["humidity"],
        "humidity_status": humidity_status,

        "overall_status": overall_status
    }