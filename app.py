"""
app.py
TrailMapInterface V3.0
Alexa Witkin
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics # from rpi-rgb-led-matrix lib
#from PIL import Image, ImageDraw, ImageFont # for led panel
import sqlite3 # included in standard python distribution
import threading
import time
import os

## ----------------------------------------------------------------------------------------
# Setup LED matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1 # increase once more panels are linked
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # Change if needed
options.gpio_slowdown = 4

matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()

# Set DISPLAY_MODE per Pi (dynamically via environment variable)
DISPLAY_MODE = os.environ.get("DISPLAY_MODE", "text")  # default to "text" if not set
print(f"Starting TrailMapInterface in {DISPLAY_MODE} mode")

display_lock = threading.Lock()

# Global for current message
current_message = "Welcome to Bromley!"
message_lock = threading.Lock()

# Get current status of the trails and lifts
current_status_snapshot = {
    "trails": {},
    "lifts": {}
}

status_lock = threading.Lock()

STATUS_COLORS = {
    "open": graphics.Color(0, 255, 0),
    "closed": graphics.Color(255, 0, 0),
    "delayed": graphics.Color(255, 255, 0)
}



## ----------------------------------------------------------------------------------------

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

# List of the trails in each panel
TRAIL_PANELS = [
    ["chase_it", "crackerjack", "learning_zone", "lower_boulevard"],
    ["lower_east_meadow", "lower_thruway", "plaza", "proutys_past"],
    ["run_around_1", "run_around_2", "run_around_3", "run_around_4"],
    ["school_slope", "woods_run", "lift_line", "lords_prayer"],
    ["lower_twister", "pushover", "ridge", "route_100"],
    ["shincracker", "snow_ranger", "spring_trail", "sunset_pass"],
    ["upper_boulevard", "upper_east_meadow", "upper_thruway", "upper_twister"],
    ["west_meadow", "yodeler", "avalanche", "blue_ribbon"],
    ["corkscrew", "havoc", "little_dipper", "lower_stargazer"],
    ["no_name_chute", "pabst_panic", "pabst_peril", "stargazer"],
    ["sunder", "the_garden", "avalanche_glade", "everglade"],
    ["orion", "spring_fling", "the_glade", "the_plunge"]
]

# List of the lifts in each panel
LIFT_PANELS = [
    ["sun_mountain_express", "plaza_chairlift", "sun_chairlift", "alpine_chairlift"],
    ["east_meadow_chairlift", "star_carpet", "blue_ribbon_quad", "lords_prayer_tbar"],
    ["kids_carpet"]
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
    with status_lock:
        current_status_snapshot["trails"] = trail_status

    return render_template("trails.html", t_stat=trail_status)

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
    with status_lock:
        current_status_snapshot["lifts"] = lift_status

    return render_template("lifts.html", l_stat=lift_status)



@app.route("/text", methods=["GET", "POST"])
def text():
    global current_message
    con = sqlite3.connect('bromley_trailmap.db', isolation_level=None)
    cur = con.cursor()

    cur.execute('SELECT status FROM Text WHERE text = "text"')
    old_text = cur.fetchone()

    if request.method == "POST":
        new_text = request.form.get("value")
        if new_text:
            cur.execute('UPDATE Text SET status = ? WHERE text = "text"', (new_text,))
            con.commit()

            # Update LED text
            with message_lock:
                current_message = new_text

    # Re-fetch updated text for rendering
    cur.execute('SELECT status FROM Text WHERE text = "text"')
    old_text = cur.fetchone()

    con.close()
    return render_template("text.html", text=old_text[0])


def scrolling_text():
    global canvas

    #os.chdir("/home/bromley/rpi-rgb-led-matrix")
    #print("CWD changed to:", os.getcwd())

    font = graphics.Font()
    font.LoadFont("/home/bromley/rpi-rgb-led-matrix/fonts/7x13.bdf")  # relative path
    print("Font loaded successfully")
    print("Current working directory:", os.getcwd())
#-------------------------------------------------------

   # font = graphics.Font()
   # font.LoadFont("fonts/7x13.bdf")
    text_color = graphics.Color(255, 0, 0)
    pos = canvas.width

    while True:
        with message_lock:
            msg = current_message

        canvas.Clear()
        text_len = graphics.DrawText(canvas, font, pos, 20, text_color, msg)
        pos -= 1
        if (pos + text_len < 0):
            pos = canvas.width

        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(0.05)

def draw_check(canvas, x, y, color):
    graphics.DrawLine(canvas, x+1, y+4, x+3, y+6, color)
    graphics.DrawLine(canvas, x+3, y+6, x+7, y+1, color)

def draw_x(canvas, x, y, color):
    graphics.DrawLine(canvas, x+1, y+1, x+6, y+6, color)
    graphics.DrawLine(canvas, x+6, y+1, x+1, y+6, color)

def draw_circle(canvas, x, y, color):
    graphics.DrawCircle(canvas, x+4, y+4, 3, color)

def draw_status_slot(canvas, x_offset, y_offset, name, status, font):
    color = STATUS_COLORS.get(status, graphics.Color(255, 255, 255))

    # Icon
    if status == "open":
        draw_check(canvas, x_offset + 2, y_offset, color)
    elif status == "closed":
        draw_x(canvas, x_offset + 2, y_offset, color)
    elif status == "delayed":
        draw_circle(canvas, x_offset + 2, y_offset, color)

    # Name
    graphics.DrawText(
        canvas,
        font,
        x_offset + 14,
        y_offset + 7,
        color,
        name.replace("_", " ").upper()
    )

def status_display():
    global canvas

    font = graphics.Font()
    font.LoadFont("/home/bromley/rpi-rgb-led-matrix/fonts/6x10.bdf")

    panels = TRAIL_PANELS if DISPLAY_MODE == "trails" else LIFT_PANELS

    while True:
        with status_lock:
            statuses = current_status_snapshot[DISPLAY_MODE]

        canvas.Clear()

        for panel_idx, panel_items in enumerate(panels):
            x_offset = panel_idx * 64

            for row_idx, name in enumerate(panel_items):
                y_offset = row_idx * 8
                status = statuses.get(name, "closed")

                draw_status_slot(canvas, x_offset, y_offset, name, status, font)

        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(0.5)

def safe_thread_loop(target_func, *args, **kwargs):
    """
    Runs a function in a loop inside a thread.
    If an exception occurs, it logs it, waits a second, and restarts the function.
    """
    while True:
        try:
            target_func(*args, **kwargs)
        except Exception as e:
            print(f"Error in thread {target_func.__name__}: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(1)  # short delay before retry



@app.route("/help")
def help():
    return render_template("help.html")

####----------START THE THREAD-------------####
# Start the display loop when the app starts
# Use safe_thread_loop to auto-recover from exceptions
if DISPLAY_MODE == "text":
    threading.Thread(target=safe_thread_loop, args=(scrolling_text,), daemon=True).start()
elif DISPLAY_MODE in ["trails", "lifts"]:
    threading.Thread(target=safe_thread_loop, args=(status_display,), daemon=True).start()



if __name__ == "__main__":
    #app.run(debug=True) # for local debugging (dev)
    app.run(host='0.0.0.0', port=5000, debug=False) # for network access

