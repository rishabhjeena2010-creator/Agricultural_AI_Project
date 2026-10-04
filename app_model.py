from flask import Flask, render_template, request, redirect, url_for
from prediction_engine import run_prediction

app = Flask(__name__)


# ============================================================
# DASHBOARD - FIRST PAGE
# ============================================================

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# ============================================================
# SELECT FARM
# ============================================================

@app.route("/select", methods=["GET", "POST"])
def select():

    if request.method == "POST":

        state = request.form["state"]
        district = request.form["district"]
        crop_type = request.form["crop_type"]

        return redirect(
            url_for(
                "farm_details",
                state=state,
                district=district,
                crop_type=crop_type
            )
        )

    return render_template("select.html")


# ============================================================
# FARM DETAILS
# ============================================================

@app.route("/farm-details", methods=["GET", "POST"])
def farm_details():

    state = request.args.get("state")
    district = request.args.get("district")
    crop_type = request.args.get("crop_type")

    if request.method == "POST":

        crop_year = int(request.form["crop_year"])

        season = request.form["season"]

        area_hectares = float(
            request.form["area_hectares"]
        )

        fertilizer_type = request.form["fertilizer_type"]

        fertilizer_amount = float(
            request.form["fertilizer_amount"]
        )

        irrigation_method = request.form[
            "irrigation_method"
        ]

        irrigation_frequency = float(
            request.form["irrigation_frequency"]
        )

        pesticide_used = request.form[
            "pesticide_used"
        ]

        pest_infection_level = request.form[
            "pest_infection_level"
        ]

        sowing_month = int(
            request.form["sowing_month"]
        )


        # ----------------------------------------------------
        # RUN PREDICTION
        # ----------------------------------------------------

        result = run_prediction(

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


        return render_template(
            "prediction.html",
            result=result
        )


    return render_template(

        "index.html",

        state=state,

        district=district,

        crop_type=crop_type
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run()
