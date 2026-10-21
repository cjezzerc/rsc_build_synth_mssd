import sys

import pyodbc

# Format for connection string (unecrytped dev connection):
# 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=???.???.???.???,???;DATABASE=???;UID=???;PWD=???;Encrypt=no;TrustServerCertificate=yes'

connection_string=sys.argv[1]
connection=pyodbc.connect(connection_string)

sql_script=open("make_trial_mssd_tables.sql").read()
cursor=connection.cursor()
cursor.execute(sql_script)
connection.commit()