#!/usr/bin/python3

import configparser
import mysql.connector

conf_file = "/content/prod/rstar/etc/my-taskqueue.cnf"

# Read the config file
config = configparser.ConfigParser()
config.read(conf_file)

# Create a connection object
cnx = mysql.connector.connect(
    host=config.get('client', 'host'),
    database=config.get('client', 'database'),
    user=config.get('client', 'user'),
    password=config.get('client', 'password'),
    connection_timeout=10
)

# Create a cursor and execute a query
cursor = cnx.cursor()
query = "SELECT * FROM job"
cursor.execute(query)

# Fetch the results
for row in cursor:
    print(row)

# Close the cursor and connection
cursor.close()
cnx.close()

