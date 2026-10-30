import sys
import tomllib
import pyodbc
import os

# Format for connection string (unecrytped dev connection):
# 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=???.???.???.???,???;DATABASE=???;UID=???;PWD=???;Encrypt=no;TrustServerCertificate=yes'

config = tomllib.load(open(sys.argv[1], "rb"))

connection_string=config["connection_string"]
connection=pyodbc.connect(connection_string)

script_dir=os.path.dirname(os.path.realpath(__file__))

sql_script=open(f"{script_dir}/make_trial_mssd_tables.sql").read()
cursor=connection.cursor()
cursor.execute(sql_script)
connection.commit()