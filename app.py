"""
app.py
TrailMapInterface V2.0
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import pwinput as pw
import sqlite3 # included in standard python distribution
import pandas as pd
import io
import serial
##import HC_05

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

    ## Chase It
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "chase_it";')
    chase_it_status = cur.fetchone() 

    ## Crackerjack
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "crackerjack";')
    crackerjack_status = cur.fetchone() 

    ## Learning Zone
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "learning_zone";')
    learning_zone_status = cur.fetchone() 

    ## Lower Boulevard
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lower_boulevard";')
    lower_boulevard_status = cur.fetchone() 

    ## Lower East Meadow
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lower_east_meadow";')
    lower_east_meadow_status = cur.fetchone() 

    ## Lower Thruway
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lower_thruway";')
    lower_thruway_status = cur.fetchone() 

    ## Plaza
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "plaza";')
    plaza_status = cur.fetchone() 

    ## Proutys Past
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "proutys_past";')
    proutys_past_status = cur.fetchone() 

    ## Run Around 1
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "run_around_1";')
    run_around_1_status = cur.fetchone() 

    ## Run Around 2
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "run_around_2";')
    run_around_2_status = cur.fetchone() 

    ## Run Around 3
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "run_around_3";')
    run_around_3_status = cur.fetchone() 

    ## Run Around 4
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "run_around_4";')
    run_around_4_status = cur.fetchone() 

    ## School Slope
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "school_slope";')
    school_slope_status = cur.fetchone() 

    ## Woods Run
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "woods_run";')
    woods_run_status = cur.fetchone() 

    ## Lift Line
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lift_line";')
    lift_line_status = cur.fetchone() 

    ## Lords Prayer
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lords_prayer";')
    lords_prayer_status = cur.fetchone() 

    ## Lower Twister
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lower_twister";')
    lower_twister_status = cur.fetchone() 

    ## Pushover
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "pushover";')
    pushover_status = cur.fetchone() 

    ## Ridge
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "ridge";')
    ridge_status = cur.fetchone() 

    ## Route 100
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "route_100";')
    route_100_status = cur.fetchone() 

    ## Shincracker
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "shincracker";')
    shincracker_status = cur.fetchone() 

    ## Snow Ranger
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "snow_ranger";')
    snow_ranger_status = cur.fetchone() 

    ## Spring Trail
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "spring_trail";')
    spring_trail_status = cur.fetchone() 

    ## Sunset Pass
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "sunset_pass";')
    sunset_pass_status = cur.fetchone() 

    ## Upper Boulevard
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "upper_boulevard";')
    upper_boulevard_status = cur.fetchone() 

    ## Upper East Meadow
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "upper_east_meadow";')
    upper_east_meadow_status = cur.fetchone() 

    ## Upper Thruway
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "upper_thruway";')
    upper_thruway_status = cur.fetchone() 

    ## Upper Twister
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "upper_twister";')
    upper_twister_status = cur.fetchone() 

    ## West Meadow
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "west_meadow";')
    west_meadow_status = cur.fetchone() 

    ## Yodeler
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "yodeler";')
    yodeler_status = cur.fetchone() 

    ## Avalanche
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "avalanche";')
    avalanche_status = cur.fetchone() 

    ## Blue Ribbon
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "blue_ribbon";')
    blue_ribbon_status = cur.fetchone() 

    ## Corkscrew
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "corkscrew";')
    corkscrew_status = cur.fetchone() 

    ## Havoc
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "havoc";')
    havoc_status = cur.fetchone() 

    ## Little Dipper 
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "little_dipper";')
    little_dipper_status = cur.fetchone() 

    ## Lower Stargazer
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lower_stargazer";')
    lower_stargazer_status = cur.fetchone() 

    ## No Name Chute
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "no_name_chute";')
    no_name_chute_status = cur.fetchone() 

    ## Pabst Panic
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "pabst_panic";')
    pabst_panic_status = cur.fetchone() 

    ## Pabst Peril
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "pabst_peril";')
    pabst_peril_status = cur.fetchone() 

    ## Stargazer
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "stargazer";')
    stargazer_status = cur.fetchone() 

    ## Sunder
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "sunder";')
    sunder_status = cur.fetchone() 

    ## The Garden
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "the_garden";')
    the_garden_status = cur.fetchone() 

    ## Avalanche Glade
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "avalanche_glade";')
    avalanche_glade_status = cur.fetchone() 

    ## Everglade
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "everglade";')
    everglade_status = cur.fetchone() 

    ## Orion
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "orion";')
    orion_status = cur.fetchone() 

    ## Spring Fling
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "spring_fling";')
    spring_fling_status = cur.fetchone() 

    ## The Glade
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "the_glade";')
    the_glade_status = cur.fetchone() 

    ## The Plunge
    cur.execute(f'SELECT status FROM Trails WHERE trail_name = "the_plunge";')
    the_plunge_status = cur.fetchone() 

    if request.method == "POST":

        ## Chase It
        new_status_0 = request.form.get("chase_it")

        if new_status_0 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_0}" WHERE trail_name = "chase_it";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "chase_it";')
            chase_it_status = cur.fetchone()

        ## Crackerjack
        new_status_1 = request.form.get("crackerjack")

        if new_status_1 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_1}" WHERE trail_name = "crackerjack";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "crackerjack";')
            crackerjack_status = cur.fetchone() 

        ## Learning Zone
        new_status_2 = request.form.get("learning_zone")

        if new_status_2 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_2}" WHERE trail_name = "learning_zone";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "learning_zone";')
            learning_zone_status = cur.fetchone() 

        ## Lower Boulevard
        new_status_3 = request.form.get("lower_boulevard")

        if new_status_3 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_3}" WHERE trail_name = "lower_boulevard";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lower_boulevard";')
            lower_boulevard_status = cur.fetchone() 

        ## Lower East Meadow
        new_status_4 = request.form.get("lower_east_meadow")

        if new_status_4 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_4}" WHERE trail_name = "lower_east_meadow";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lower_east_meadow";')
            lower_east_meadow_status = cur.fetchone() 

        ## Lower Thruway
        new_status_5 = request.form.get("lower_thruway")

        if new_status_5 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_5}" WHERE trail_name = "lower_thruway";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lower_thruway";')
            lower_thruway_status = cur.fetchone() 

        ## Plaza
        new_status_6 = request.form.get("plaza")

        if new_status_6 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_6}" WHERE trail_name = "plaza";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "plaza";')
            plaza_status = cur.fetchone() 

        ## Proutys Past
        new_status_7 = request.form.get("proutys_past")

        if new_status_7 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_7}" WHERE trail_name = "proutys_past";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "proutys_past";')
            proutys_past_status = cur.fetchone() 

        ## Run Around 1
        new_status_8 = request.form.get("run_around_1")

        if new_status_8 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_8}" WHERE trail_name = "run_around_1";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "run_around_1";')
            run_around_1_status = cur.fetchone() 

        ## Run Around 2
        new_status_9 = request.form.get("run_around_2")

        if new_status_9 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_9}" WHERE trail_name = "run_around_2";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "run_around_2";')
            run_around_2_status = cur.fetchone() 

        ## Run Around 3
        new_status_10 = request.form.get("run_around_3")

        if new_status_10 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_10}" WHERE trail_name = "run_around_3";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "run_around_3";')
            run_around_3_status = cur.fetchone() 

        ## Run Around 4
        new_status_11 = request.form.get("run_around_4")

        if new_status_11 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_11}" WHERE trail_name = "run_around_4";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "run_around_4";')
            run_around_4_status = cur.fetchone() 

        ## School Slope
        new_status_12 = request.form.get("school_slope")

        if new_status_12 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_12}" WHERE trail_name = "school_slope";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "school_slope";')
            school_slope_status = cur.fetchone() 

        ## Woods Run
        new_status_13 = request.form.get("woods_run")

        if new_status_13 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_13}" WHERE trail_name = "woods_run";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "woods_run";')
            woods_run_status = cur.fetchone() 

        ## Lift Line
        new_status_14 = request.form.get("lift_line")

        if new_status_14 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_14}" WHERE trail_name = "lift_line";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lift_line";')
            lift_line_status = cur.fetchone() 

        ## Lords Prayer
        new_status_15 = request.form.get("lords_prayer")

        if new_status_15 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_15}" WHERE trail_name = "lords_prayer";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lords_prayer";')
            lords_prayer_status = cur.fetchone() 

        ## Lower Twister 
        new_status_16 = request.form.get("lower_twister")

        if new_status_16 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_16}" WHERE trail_name = "lower_twister";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lower_twister";')
            lower_twister_status = cur.fetchone() 

        ## Pushover
        new_status_17 = request.form.get("pushover")

        if new_status_17 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_17}" WHERE trail_name = "pushover";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "pushover";')
            pushover_status = cur.fetchone() 
        
        ## Ridge
        new_status_18 = request.form.get("ridge")

        if new_status_18 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_18}" WHERE trail_name = "ridge";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "ridge";')
            ridge_status = cur.fetchone() 

        ## Route 100
        new_status_19 = request.form.get("route_100")

        if new_status_19 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_19}" WHERE trail_name = "route_100";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "route_100";')
            route_100_status = cur.fetchone() 

        ## Shincracker
        new_status_20 = request.form.get("shincracker")

        if new_status_20 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_20}" WHERE trail_name = "shincracker";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "shincracker";')
            shincracker_status = cur.fetchone() 

        ## Snow Ranger
        new_status_21 = request.form.get("snow_ranger")

        if new_status_21 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_21}" WHERE trail_name = "snow_ranger";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "snow_ranger";')
            snow_ranger_status = cur.fetchone() 

        ## Spring Trail
        new_status_22 = request.form.get("spring_trail")

        if new_status_22 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_22}" WHERE trail_name = "spring_trail";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "spring_trail";')
            spring_trail_status = cur.fetchone() 

        ## Sunset Pass
        new_status_23 = request.form.get("sunset_pass")

        if new_status_23 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_23}" WHERE trail_name = "sunset_pass";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "sunset_pass";')
            sunset_pass_status = cur.fetchone() 

        ## Upper Boulevard
        new_status_24 = request.form.get("upper_boulevard")

        if new_status_24 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_24}" WHERE trail_name = "upper_boulevard";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "upper_boulevard";')
            upper_boulevard_status = cur.fetchone() 

        ## Upper East Meadow
        new_status_25 = request.form.get("upper_east_meadow")

        if new_status_25 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_25}" WHERE trail_name = "upper_east_meadow";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "upper_east_meadow";')
            upper_east_meadow_status = cur.fetchone() 

        ## Upper Thruway
        new_status_26 = request.form.get("upper_thruway")

        if new_status_26 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_26}" WHERE trail_name = "upper_thruway";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "upper_thruway";')
            upper_thruway_status = cur.fetchone() 

        ## Upper Twister
        new_status_27 = request.form.get("upper_twister")

        if new_status_27 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_27}" WHERE trail_name = "upper_twister";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "upper_twister";')
            upper_twister_status = cur.fetchone() 

        ## West Meadow
        new_status_28 = request.form.get("west_meadow")

        if new_status_28 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_28}" WHERE trail_name = "west_meadow";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "west_meadow";')
            west_meadow_status = cur.fetchone() 

        ## Yodeler
        new_status_29 = request.form.get("yodeler")

        if new_status_29 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_29}" WHERE trail_name = "yodeler";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "yodeler";')
            yodeler_status = cur.fetchone() 

        ## Avalanche
        new_status_30 = request.form.get("avalanche")

        if new_status_30 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_30}" WHERE trail_name = "avalanche";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "avalanche";')
            avalanche_status = cur.fetchone() 

        ## Blue Ribbon
        new_status_31 = request.form.get("blue_ribbon")

        if new_status_31 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_31}" WHERE trail_name = "blue_ribbon";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "blue_ribbon";')
            blue_ribbon_status = cur.fetchone()

        ## Corkscrew
        new_status_32 = request.form.get("corkscrew")

        if new_status_32 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_32}" WHERE trail_name = "corkscrew";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "corkscrew";')
            corkscrew_status = cur.fetchone()

        ## Havoc
        new_status_33 = request.form.get("havoc")

        if new_status_33 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_33}" WHERE trail_name = "havoc";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "havoc";')
            havoc_status = cur.fetchone()

        ## Little Dipper 
        new_status_34 = request.form.get("little_dipper")

        if new_status_34 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_34}" WHERE trail_name = "little_dipper";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "little_dipper";')
            little_dipper_status = cur.fetchone()

        ## Lower Stargazer 
        new_status_35 = request.form.get("lower_stargazer")

        if new_status_35 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_35}" WHERE trail_name = "lower_stargazer";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "lower_stargazer";')
            lower_stargazer_status = cur.fetchone()

        ## No Name Chute 
        new_status_36 = request.form.get("no_name_chute")

        if new_status_36 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_36}" WHERE trail_name = "no_name_chute";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "no_name_chute";')
            no_name_chute_status = cur.fetchone()

        ## Pabst Panic
        new_status_37 = request.form.get("pabst_panic")

        if new_status_37 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_37}" WHERE trail_name = "pabst_panic";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "pabst_panic";')
            pabst_panic_status = cur.fetchone()

        ## Pabst Peril
        new_status_38 = request.form.get("pabst_peril")

        if new_status_38 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_38}" WHERE trail_name = "pabst_peril";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "pabst_peril";')
            pabst_peril_status = cur.fetchone()

        ## Stargazer
        new_status_39 = request.form.get("stargazer")

        if new_status_39 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_39}" WHERE trail_name = "stargazer";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "stargazer";')
            stargazer_status = cur.fetchone()

        ## Sunder
        new_status_40 = request.form.get("sunder")

        if new_status_40 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_40}" WHERE trail_name = "sunder";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "sunder";')
            sunder_status = cur.fetchone()

        ## The Garden
        new_status_41 = request.form.get("the_garden")

        if new_status_41 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_41}" WHERE trail_name = "the_garden";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "the_garden";')
            the_garden_status = cur.fetchone()

        ## Avalanche Glade
        new_status_42 = request.form.get("avalanche_glade")

        if new_status_42 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_42}" WHERE trail_name = "avalanche_glade";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "avalanche_glade";')
            avalanche_glade_status = cur.fetchone()

        ## Everglade
        new_status_43 = request.form.get("everglade")

        if new_status_43 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_43}" WHERE trail_name = "everglade";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "everglade";')
            everglade_status = cur.fetchone()

        ## Orion
        new_status_44 = request.form.get("orion")

        if new_status_44 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_44}" WHERE trail_name = "orion";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "orion";')
            orion_status = cur.fetchone()

        ## Spring Fling
        new_status_45 = request.form.get("spring_fling")

        if new_status_45 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_45}" WHERE trail_name = "spring_fling";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "spring_fling";')
            spring_fling_status = cur.fetchone()

        ## The Glade
        new_status_46 = request.form.get("the_glade")

        if new_status_46 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_46}" WHERE trail_name = "the_glade";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "the_glade";')
            the_glade_status = cur.fetchone()

        ## The Plunge
        new_status_47 = request.form.get("the_plunge")

        if new_status_47 != None:
            cur.execute(f'UPDATE Trails SET status = "{new_status_47}" WHERE trail_name = "the_plunge";')
            con.commit()

            cur.execute(f'SELECT status FROM Trails WHERE trail_name = "the_plunge";')
            the_plunge_status = cur.fetchone()

    trail_status = []
    trail_status = get_trail_status()
    print(trail_status)

    # print(f"Chase It: " + chase_it_status[0])
    # print(f"Crackerjack: " + crackerjack_status[0])
    # print(f"Learning Zone: " + learning_zone_status[0])
    # print(f"Lower Boulevard: " + lower_boulevard_status[0])
    # print(f"Lower East Meadow: " + lower_east_meadow_status[0])
    # print(f"Lower Thruway: " + lower_thruway_status[0])
    # print(f"Plaza: " + plaza_status[0])
    # print(f"Prouty's Past: " + proutys_past_status[0])
    # print(f"Run Around 1: " + run_around_1_status[0])
    # print(f"Run Around 2: " + run_around_2_status[0])
    # print(f"Run Around 3: " + run_around_3_status[0])
    # print(f"Run Around 4: " + run_around_4_status[0])
    # print(f"School Slope: " + school_slope_status[0])
    # print(f"Woods Run: " + woods_run_status[0])
    # print(f"Lift Line: " + lift_line_status[0])
    # print(f"Lords Prayer: " + lords_prayer_status[0])
    # print(f"Lower Twister: " + lower_twister_status[0])
    # print(f"Pushover: " + pushover_status[0])
    # print(f"Ridge: " + ridge_status[0])
    # print(f"Route 100: " + route_100_status[0])
    # print(f"Shincracker: " + shincracker_status[0])
    # print(f"Snow Ranger: " + snow_ranger_status[0])
    # print(f"Spring Trail: " + spring_trail_status[0])
    # print(f"Sunset Pass: " + sunset_pass_status[0])
    # print(f"Upper Boulevard: " + upper_boulevard_status[0])
    # print(f"Upper East Meadow: " + upper_east_meadow_status[0])
    # print(f"Upper Thruway: " + upper_thruway_status[0])
    # print(f"Upper Twister: " + upper_twister_status[0])
    # print(f"West Meadow: " + west_meadow_status[0])
    # print(f"Yodeler: " + yodeler_status[0])
    # print(f"Avalanche: " + avalanche_status[0])
    # print(f"Blue Ribbon: " + blue_ribbon_status[0])
    # print(f"Corkscrew: " + corkscrew_status[0])
    # print(f"Havoc: " + havoc_status[0])
    # print(f"Little Dipper: " + little_dipper_status[0])
    # print(f"Lower Stargazer: " + lower_stargazer_status[0])
    # print(f"No Name Chute: " + no_name_chute_status[0])
    # print(f"Pabst Panic: " + pabst_panic_status[0])
    # print(f"Pabst Peril: " + pabst_peril_status[0])
    # print(f"Stargazer: " + stargazer_status[0])
    # print(f"Sunder: " + sunder_status[0])
    # print(f"The Garden: " + the_garden_status[0])
    # print(f"Avalanche Glade: " + avalanche_glade_status[0])
    # print(f"Everglade: " + everglade_status[0])
    # print(f"Orion: " + orion_status[0])
    # print(f"Spring Trail: " + spring_fling_status[0])
    # print(f"Sunset Pass: " + sunset_pass_status[0])
    # print(f"The Glade: " + the_glade_status[0])
    # print(f"The Plunge: " + the_plunge_status[0])

    ##HC_05.chaseIt_open()
    return render_template("trails.html", t_stat=trail_status)


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
