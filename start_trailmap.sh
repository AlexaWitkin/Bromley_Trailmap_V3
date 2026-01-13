#!/bin/bash

# ---------------------------------------------------------
# TrailMap Startup Script
# Runs app.py inside virtual environment
# ---------------------------------------------------------

# Wait a few seconds for network to come up
sleep 10

# Navigate to the project directory
cd /home/bromley/Bromley_Trailmap_V3

# Activate the virtual environment
source /home/bromley/myenv/bin/activate

# Automatically set DISPLAY_MODE based on Pi hostname
HOSTNAME=$(hostname)
case "$HOSTNAME" in
    bromleypi)
        export DISPLAY_MODE=text
        ;;
    trailspi)
        export DISPLAY_MODE=trails
        ;;
    liftspi)
        export DISPLAY_MODE=lifts
        ;;
    *)
        echo "Unknown Pi hostname: $HOSTNAME. Defaulting to text mode."
        export DISPLAY_MODE=text
        ;;
esac

# Run the Flask app
# Using sudo ONLY if necessary for hardware access
/home/bromley/myenv/bin/python app.py


# TO MAKE IT EXECUTABLE ENTER BELOW IN TERMINAL ------------------
# chmod +x /home/bromley/start_trailmap.sh