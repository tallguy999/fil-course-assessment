import pandas as pd
import mysql.connector as sql
import my_functions as myfunctions
db_connection = sql.connect(user='me0RUcEKLC',password='NYzWbTM2H6',host='remotemysql.com',database='me0RUcEKLC')
pd.options.display.max_columns = 50

inner_boroughs = ['Camden','City of London','Hackney','Hammersmith and Fulham','Haringey','Islington','Kensington and Chelsea','Lambeth','Lewisham','Newham','Southwark','Tower Hamlets','Wandsworth','Westminster']
outer_boroughs = ['Barking and Dagenham','Barnet','Bexley','Brent','Bromley','Croydon','Ealing','Enfield','Greenwich','Harrow','Havering','Hillingdon','Hounslow','Kingston upon Thames','Merton','Redbridge','Richmond upon Thames','Sutton','Waltham Forest']
boroughs = inner_boroughs + outer_boroughs

# 2. Importing Data
# Read in the crimes data. We are only interested in the Crime Type and the Borough in which it was committed
df_crimes = pd.read_csv('sample_crimes.csv', usecols=['LSOA name', 'Crime type'])

df_profiles = myfunctions.Process_Profiles('London-Borough-Profiles.csv')
df_keyindicators = pd.read_sql('SELECT * FROM KEY_INDICATORS', con=db_connection)


# Split out the Region 'LSOA name', create the 'Borough' column, then drop the original 'LSOA name'
result = df_crimes['LSOA name'].str.rpartition()
df_crimes['Borough'] = result[0]
df_crimes.drop('LSOA name', axis=1, inplace=True)

# Drop all the rows that aren't committed within a London borough
df_crimes = df_crimes[df_crimes['Borough'].isin(boroughs)]

# Summarise the crime data by counting the total crimes by borough.
# df = df_crimes.groupby(['Borough'])['Crime type'].count()
df = df_crimes.groupby(['Borough']).count()

# Merge the profiles data with the borough / crime data
# Then merge again with the Key Indicators data
df = pd.merge(df, df_profiles, on="Borough",how="left")
df = pd.merge(df, df_keyindicators, on="Borough",how="left")
# The Area(Hectares) column has commas as thousand-separators. Remove these using RegEx.
df = df.replace(to_replace=r',',value='',regex=True)

# Rename the 'Crime type' column to 'Crime Count'
df.rename(columns = {'Crime type':'Crime Count'}, inplace = True)

myfunctions.ExportToCSV(df, 'test2')











