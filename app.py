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
##import HC_05

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

app = Flask(__name__)
##bluetooth = serial.Serial("/dev/rfcomm2", 9600) # send serial value

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

    trail_status = []
    trail_status = get_trail_status()
    print(trail_status)

    lift_status = []
    lift_status = get_lift_status()
    print(lift_status)
    
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

    trail_status = []
    trail_status = get_trail_status()
    print(trail_status)

    lift_status = []
    lift_status = get_lift_status()
    print(lift_status)

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

    # # Convert to dict for easier use in template
    # trail_status = {row['trail_name']: row['status'] for row in trails_statuses}
    # Assuming SELECT trail_name, status returns two columns:
    trail_status = {row[0]: row[1] for row in trails_statuses}

    return render_template("trails.html", t_stat=trail_status)

# Add a simple route that returns all trail statuses as JSON, which the Pi can poll regularly
@app.route('/api/trail_statuses', methods=['GET'])
def api_trail_statuses():
    con = sqlite3.connect('bromley_trailmap.db', isolation_level=None)
    cur = con.cursor()
    cur.execute('SELECT trail_name, status FROM Trails')
    rows = cur.fetchall()
    con.close()

    # Convert rows to dict
    statuses = {row['trail_name']: row['status'] for row in rows}
    return jsonify(statuses)


@app.route("/lifts", methods=["GET","POST"])
def lifts():
    con = sqlite3.connect('bromley_trailmap.db', isolation_level=None)
    cur = con.cursor()

    ## Sun Mountain Express
    cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "sun_mountain_express";')
    sun_mountain_express_status = cur.fetchone()

    ## Plaza Chairlift
    cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "plaza_chairlift";')
    plaza_chairlift_status = cur.fetchone()

    ## Sun Chairlift
    cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "sun_chairlift";')
    sun_chairlift_status = cur.fetchone()

    ## Alpine Chairlift
    cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "alpine_chairlift";')
    alpine_chairlift_status = cur.fetchone()

    ## East Meadow Chairlift
    cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "east_meadow_chairlift";')
    east_meadow_chairlift_status = cur.fetchone()

    ## Star Carpet
    cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "star_carpet";')
    star_carpet_status = cur.fetchone()

    ## Blue Ribbon Quad
    cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "blue_ribbon_quad";')
    blue_ribbon_quad_status = cur.fetchone()

    ## Lords Prayer Tbar
    cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "lords_prayer_tbar";')
    lords_prayer_tbar_status = cur.fetchone()

    ## Kids Carpet
    cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "kids_carpet";')
    kids_carpet_status = cur.fetchone()

    if request.method == "POST":

        ## Sun Mountain Express
        new_status_0 = request.form.get("sun_mountain_express")

        if new_status_0 != None:
            cur.execute(f'UPDATE Lifts SET status = "{new_status_0}" WHERE lift_name = "sun_mountain_express";')
            con.commit()

            cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "sun_mountain_express";')
            sun_mountain_express_status = cur.fetchone()

        ## Plaza Chairlift
        new_status_1 = request.form.get("plaza_chairlift")

        if new_status_1 != None:
            cur.execute(f'UPDATE Lifts SET status = "{new_status_1}" WHERE lift_name = "plaza_chairlift";')
            con.commit()

            cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "plaza_chairlift";')
            plaza_chairlift_status = cur.fetchone()

        ## Sun Chairlift
        new_status_2 = request.form.get("sun_chairlift")

        if new_status_2 != None:
            cur.execute(f'UPDATE Lifts SET status = "{new_status_2}" WHERE lift_name = "sun_chairlift";')
            con.commit()

            cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "sun_chairlift";')
            sun_chairlift_status = cur.fetchone()

        ## Alpine Chairlift
        new_status_3 = request.form.get("alpine_chairlift")

        if new_status_3 != None:
            cur.execute(f'UPDATE Lifts SET status = "{new_status_3}" WHERE lift_name = "alpine_chairlift";')
            con.commit()

            cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "alpine_chairlift";')
            alpine_chairlift_status = cur.fetchone()

        ## East Meadow Chairlift
        new_status_4 = request.form.get("east_meadow_chairlift")

        if new_status_4 != None:
            cur.execute(f'UPDATE Lifts SET status = "{new_status_4}" WHERE lift_name = "east_meadow_chairlift";')
            con.commit()

            cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "east_meadow_chairlift";')
            east_meadow_chairlift_status = cur.fetchone()

        ## Star Carpet
        new_status_5 = request.form.get("star_carpet")

        if new_status_5 != None:
            cur.execute(f'UPDATE Lifts SET status = "{new_status_5}" WHERE lift_name = "star_carpet";')
            con.commit()

            cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "star_carpet";')
            star_carpet_status = cur.fetchone()

        ## Blue Ribbon Quad
        new_status_6 = request.form.get("blue_ribbon_quad")

        if new_status_6 != None:
            cur.execute(f'UPDATE Lifts SET status = "{new_status_6}" WHERE lift_name = "blue_ribbon_quad";')
            con.commit()

            cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "blue_ribbon_quad";')
            blue_ribbon_quad_status = cur.fetchone()

        ## Lords Prayer Tbar
        new_status_7 = request.form.get("lords_prayer_tbar")

        if new_status_7 != None:
            cur.execute(f'UPDATE Lifts SET status = "{new_status_7}" WHERE lift_name = "lords_prayer_tbar";')
            con.commit()

            cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "lords_prayer_tbar";')
            lords_prayer_tbar_status = cur.fetchone()

        ## Kids Carpet
        new_status_8 = request.form.get("kids_carpet")

        if new_status_8 != None:
            cur.execute(f'UPDATE Lifts SET status = "{new_status_8}" WHERE lift_name = "kids_carpet";')
            con.commit()

            cur.execute(f'SELECT status FROM Lifts WHERE lift_name = "kids_carpet";')
            kids_carpet_status = cur.fetchone()
    
    get_trail_status()
    get_lift_status()

    lift_status = []
    lift_status = get_lift_status()
    print(lift_status)

    # print(f"Sun Mountain Express: " + sun_mountain_express_status[0])
    # print(f"Plaza Chair: " + plaza_chairlift_status[0])
    # print(f"Sun Chairlift: " + sun_chairlift_status[0])
    # print(f"Alpine Chairlift: " + alpine_chairlift_status[0])
    # print(f"East Meadow Chairlift: " + east_meadow_chairlift_status[0])
    # print(f"Star Carpet: " + star_carpet_status[0])
    # print(f"Blue Ribbon Quad: " + blue_ribbon_quad_status[0])
    # print(f"Lords Prayer Tbar: " + lords_prayer_tbar_status[0])
    # print(f"Kids Carpet: " + kids_carpet_status[0])

    ##HC_05.chaseIt_open()
    return render_template("lifts.html", l_stat=lift_status)


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

    get_trail_status()
    get_lift_status()

    return render_template("text.html", text=old_text[0])

@app.route("/help")
def help():
    return render_template("help.html")

def get_trail_status():
    con = sqlite3.connect('bromley_trailmap.db', isolation_level=None)
    cur = con.cursor()

    ## Trails
    cur.execute(f'SELECT status FROM Trails;')
    trails = cur.fetchall()

    trail_status = []
    for i in range(0,len(trails)):
        trail_status.append(trails[i][0])
    print(trail_status)

    arduino_trail_status = []
    for i in range(0,len(trail_status)):
        if trail_status[i] == 'open':
            arduino_trail_status.append(100)
        elif trail_status[i] == 'delayed':
            arduino_trail_status.append(200)
        elif trail_status[i] == 'closed':
            arduino_trail_status.append(300)
    print(arduino_trail_status)

    return arduino_trail_status


def get_lift_status():
    con = sqlite3.connect('bromley_trailmap.db', isolation_level=None)
    cur = con.cursor()

    ## Lifts
    cur.execute(f'SELECT status FROM Lifts;')
    lifts = cur.fetchall()

    lift_status = []
    for i in range(0,len(lifts)):
        lift_status.append(lifts[i][0])
    print(lift_status)

    arduino_lift_status = []
    for i in range(0,len(lift_status)):
        if lift_status[i] == 'open':
            arduino_lift_status.append(100)
        elif lift_status[i] == 'delayed':
            arduino_lift_status.append(200)
        elif lift_status[i] == 'closed':
            arduino_lift_status.append(300)
    print(arduino_lift_status)

    return arduino_lift_status

    


# # Sends a serial code 'a' to Arduino
# def send_bluetooth_data(a):
#     string = 'X{0}'.format(a) # format of our data
#     print('Serial code:' + string)
#     bluetooth.write(string.encode("utf-8"))

#     get_trail_status()
#     get_lift_status()


if __name__ == "__main__":
    app.run(debug=True)

    # while True:
    #     a = input("enter: -") # input value to be received by arduino bluetooth
    #     ''' this is where we can determine what pins we want on to control each
    #     component independently '''

    #     send_bluetooth_data(a)
