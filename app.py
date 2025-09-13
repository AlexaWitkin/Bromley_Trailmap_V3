"""
app.py
TrailMapInterface V3.0
Alexa Witkin
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
##from rgbmatrix import RGBMatrix, RGBMatrixOptions # from rpi-rgb-led-matrix lib
from PIL import Image, ImageDraw, ImageFont # for led panel
import pwinput as pw
import sqlite3 # included in standard python distribution
import pandas as pd
import io
import serial

# List of all trail names
TRAIL_NAMES = [
    "chase_it", "crackerjack", "learning_zone", "lower_boulevard", "lower_east_meadow",
    "lower_thruway", "plaza", "proutys_past", "run_around_1", "run_around_2", "run_around_3",
    "run_around_4", "school_slope", "woods_run", "lift_line", "lords_prayer", "lower_twister",
    "pushover", "ridge", "route_100", "shincracker", "snow_ranger", "spring_trail", "sunset_pass",
    "upper_boulevard", "upper_east_meadow", "upper_thruway", "upper_twister", "west_meadow",
    "yodeler", "avalanche", "blue_ribbon", "corkscrew", "havoc", "little_dipper",
    "lower_stargazer", "no_name_chute", "pabst_panic", "pabst_peril", "stargazer", "sunder",
    "the_garden", "avalanche_glade", "everglade", "orion", "spring_fling", "the_glade",
    "the_plunge"
]

# List of all lift names
LIFT_NAMES = [
    "sun_mountain_express", "plaza_chairlift", "sun_chairlift", "alpine_chairlift",
    "east_meadow_chairlift", "star_carpet", "blue_ribbon_quad", "lords_prayer_tbar",
    "kids_carpet"
]

app = Flask(__name__)

@app.route("/")
def index():
    '''
    home page.
    '''
    con = sqlite3.connect('bromley_trailmap.db', isolation_level=None)
    cur = con.cursor()

    ## Trails
    cur.execute(f'SELECT trail_name, status FROM Trails;')
    trail_data = cur.fetchall()
    trail_columns = ["trail", "status"]
    trail_formatted_data = [dict(zip(trail_columns, row)) for row in trail_data]
    print(trail_formatted_data)

    ## Lifts 
    cur.execute(f'SELECT lift_name, status FROM Lifts;')
    lift_data = cur.fetchall()
    lift_columns = ["lift", "status"]
    lift_formatted_data = [dict(zip(lift_columns, row)) for row in lift_data]
    print(lift_formatted_data)

    return render_template("home.html", t_data=trail_formatted_data, l_data=lift_formatted_data)



@app.route("/home", methods=["GET", "POST"])
def home():
    '''
    home page.
    '''
    con = sqlite3.connect('bromley_trailmap.db', isolation_level=None)
    cur = con.cursor()

    ## Trails
    cur.execute(f'SELECT trail_name, status FROM Trails;')
    trail_data = cur.fetchall()
    trail_columns = ["trail", "status"]
    trail_formatted_data = [dict(zip(trail_columns, row)) for row in trail_data]
    print(trail_formatted_data)

    ## Lifts 
    cur.execute(f'SELECT lift_name, status FROM Lifts;')
    lift_data = cur.fetchall()
    lift_columns = ["lift", "status"]
    lift_formatted_data = [dict(zip(lift_columns, row)) for row in lift_data]
    print(lift_formatted_data)

    return render_template("home.html", t_data=trail_formatted_data, l_data=lift_formatted_data)


@app.route("/trails", methods=["GET","POST"])
def trails():
    con = sqlite3.connect('bromley_trailmap.db', isolation_level=None)
    cur = con.cursor()

    if request.method == "POST":
        for trail_name in TRAIL_NAMES:
            new_status = request.form.get(trail_name)
            if new_status is not None:
                # Use parameterized queries to avoid SQL injection
                cur.execute('UPDATE Trails SET status = ? WHERE trail_name = ?', (new_status, trail_name))
                con.commit()

        # After update, get all statuses to pass to template
        cur.execute('SELECT trail_name, status FROM Trails')
        trails_statuses = cur.fetchall()
    else:
        # GET request - just fetch all trail statuses
        cur.execute('SELECT trail_name, status FROM Trails')
        trails_statuses = cur.fetchall()

    con.close()

    # Assuming SELECT trail_name, status returns two columns:
    trail_status = {row[0]: row[1] for row in trails_statuses}

    return render_template("trails.html", t_stat=trail_status)

## TODO: write correct api integrations with raspberrypi for trails
# Add a simple route that returns all trail statuses as JSON, which the Pi can poll regularly
@app.route('/api/trail_statuses', methods=['GET'])
def api_trail_statuses():
    con = sqlite3.connect('bromley_trailmap.db', isolation_level=None)
    cur = con.cursor()
    cur.execute('SELECT trail_name, status FROM Trails')
    rows = cur.fetchall()
    con.close()

    # Convert list of tuples into dict: {trail_name: status, ...}
    statuses = {row[0]: row[1] for row in rows}
    return jsonify(statuses)


@app.route("/lifts", methods=["GET","POST"])
def lifts():
    con = sqlite3.connect('bromley_trailmap.db', isolation_level=None)
    cur = con.cursor()

    if request.method == "POST":
        for lift_name in LIFT_NAMES:
            new_status = request.form.get(lift_name)
            if new_status is not None:
                cur.execute('UPDATE Lifts SET status = ? WHERE lift_name = ?', (new_status, lift_name))
                con.commit()

    cur.execute('SELECT lift_name, status FROM Lifts')
    rows = cur.fetchall()
    con.close()

    # Use tuple indexes
    lift_status = {row[0]: row[1] for row in rows}

    return render_template("lifts.html", l_stat=lift_status)

## TODO: write correct api integrations with raspberrypi for lifts

@app.route('/api/lift_statuses', methods=['GET'])
def api_lift_statuses():
    con = sqlite3.connect('bromley_trailmap.db')
    cur = con.cursor()
    cur.execute('SELECT lift_name, status FROM Lifts')
    rows = cur.fetchall()
    con.close()

    # Convert list of tuples into dict: {lift_name: status, ...}
    statuses = {row[0]: row[1] for row in rows}
    return jsonify(statuses)


@app.route("/text", methods=["GET","POST"])
def text():
    con = sqlite3.connect('bromley_trailmap.db', isolation_level=None)
    cur = con.cursor()

    cur.execute(f'SELECT status FROM Text WHERE text = "text";')
    old_text = cur.fetchone()
    print(old_text[0])

    if request.method == "POST":
        new_text = request.form.get("value", None)
        print(new_text)

        cur.execute(f'SELECT status FROM Text WHERE text = "text";')
        old_text = cur.fetchone()

        cur.execute(f'UPDATE Text SET status = "{new_text}" WHERE text = "text";')
        con.commit()

    cur.execute(f'SELECT status FROM Text WHERE text = "text";')
    old_text = cur.fetchone()
    print(old_text[0])

    return render_template("text.html", text=old_text[0])

## TODO: write correct api integrations with raspberrypi for scrolling text


@app.route("/help")
def help():
    return render_template("help.html")



if __name__ == "__main__":
    app.run(debug=True)

