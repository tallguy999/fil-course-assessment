import pandas as pd
import mysql.connector as sql

db_connection = sql.connect(user='me0RUcEKLC',password='NYzWbTM2H6',host='remotemysql.com',database='me0RUcEKLC')
pd.options.display.max_columns = 50

# Use the 'usecols' parameter to only bring in the columns we need.
df_crimes = pd.read_csv('data/sample_crimes.csv', usecols=['Crime ID', 'Month', 'LSOA name', 'Crime type', 'Last outcome category'])
df_outcomes =  pd.read_csv('data/sample_outcomes.csv', usecols=['Crime ID', 'Outcome type'])

df_keyindicators = pd.read_sql('SELECT * FROM KEY_INDICATORS', con=db_connection)

# By default, the Month columns contains the year and month in the format yyyy-mm
# Create a new Year column from the Month column and
# update the Month column so that it only contains the Month value,

df_crimes['Year'] =  df_crimes.Month.str.slice(0,4)
df_crimes['Month'] = df_crimes.Month.str.slice(5)

# Split the 'LSOA name' column using rpartition()
# rpartition results in a dataframe ('result') comprising 3 columns;
# [0] The Region [1] A Space [2] The LSOA Code
# Use column [0] to create a new Region column

result = df_crimes['LSOA name'].str.rpartition()
df_crimes['Region'] = result[0]

# Count Crimes by Region then Sort Descending
# The top 33 values should contain all the London Boroughs
region_summary = df_crimes.groupby(['Region']).Region.count()
sorted_region_summary = region_summary.sort_values(ascending=False)
data = sorted_region_summary.head(33)
boroughs = data.index.to_list()

# Use the boroughs list to filter the original crimes data frame
df_crimes_filtered = df_crimes[df_crimes['Region'].isin(boroughs)]

# Check to see what we are left with. By doing a count of unique values in the Regions column
# we should be left with only crimes with London Boroughs specified (33 in total)
print(df_crimes.shape)
print(df_crimes_filtered.shape)
print(df_crimes_filtered['Region'].value_counts())

# Next we want to filter out anything WITHOUT a CrimeID, as without that we can't determine an outcome
# from the Outcomes data
print("Before DropNA on Crime ID column")
print(df_crimes_filtered.shape)
df_crimes_filtered = df_crimes_filtered.dropna(subset=['Crime ID'])
print("After DropNA on Crime ID column")
print(df_crimes_filtered.shape)





