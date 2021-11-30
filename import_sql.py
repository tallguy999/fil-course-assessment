# Importing Data From a Remote SQL Database
# This script uses Pandas to retrieve data and create a dataframe from the result
# Steve Collins 30th November 2021

import mysql.connector as sql
import pandas as pd

db_connection = sql.connect(user='me0RUcEKLC',password='NYzWbTM2H6',host='remotemysql.com',database='me0RUcEKLC')
df = pd.read_sql('SELECT * FROM KEY_INDICATORS', con=db_connection)

print(df.columns)
print(df.shape)
print(df.info)







