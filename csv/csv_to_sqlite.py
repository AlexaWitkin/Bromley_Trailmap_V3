# Alexa Witkin
# CS 2500

import sqlite3 # included in standard python distribution
import pandas as pd

# create new database
con = sqlite3.connect('../bromley_trailmap.db')
cur = con.cursor()

# load customers.csv into database
cur.execute("DROP TABLE IF EXISTS Trails;")
users = pd.read_csv('Trails.csv')
users.to_sql('Trails', con, if_exists='replace')

# load plates.csv into database
cur.execute("DROP TABLE IF EXISTS Lifts;")
users = pd.read_csv('Lifts.csv')
users.to_sql('Lifts', con, if_exists='replace')

# load liveData.csv into database
cur.execute("DROP TABLE IF EXISTS Text;")
users = pd.read_csv('Text.csv')
users.to_sql('Text', con, if_exists='replace')


con.commit()