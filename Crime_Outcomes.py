import pandas as pd
import mysql.connector as sql
import openpyxl

db_connection = sql.connect(user='me0RUcEKLC',password='NYzWbTM2H6',host='remotemysql.com',database='me0RUcEKLC')
pd.options.display.max_columns = 50

# Use the 'usecols' parameter to only bring in the columns we need.
df_crimes = pd.read_csv('sample_crimes.csv', usecols=['Crime ID', 'Month', 'LSOA name', 'Crime type', 'Last outcome category'])
df_outcomes =  pd.read_csv('sample_outcomes.csv', usecols=['Crime ID', 'Outcome type'])
df_keyindicators = pd.read_sql('SELECT * FROM KEY_INDICATORS', con=db_connection)

# By default, the Month columns contains the year and month in the format yyyy-mm
# Create a new Year column from the Month column and
# update the Month column so that it only contains the Month value,

df_crimes['Year'] =  df_crimes.Month.str.slice(0,4)
df_crimes['Month'] = df_crimes.Month.str.slice(5)

# Split the 'LSOA name' column using rpartition()
# rpartition results in a dataframe ('result') comprising 3 columns;
# [0] The Region [1] A Space [2] The LSOA Code
# Use column [0] to create a new Borough column

result = df_crimes['LSOA name'].str.rpartition()
df_crimes['Borough'] = result[0]

# Count Crimes by Borough then Sort Descending
# The top 33 values should contain all the London Boroughs
Borough_summary = df_crimes.groupby(['Borough']).Borough.count()
sorted_Borough_summary = Borough_summary.sort_values(ascending=False)
data = sorted_Borough_summary.head(33)
boroughs = data.index.to_list()

# Use the boroughs list to filter the original crimes data frame
df_crimes_filtered = df_crimes[df_crimes['Borough'].isin(boroughs)]

# Check to see what we are left with. By doing a count of unique values in the Borough column
# we should be left with only crimes with London Boroughs specified (33 in total)
print(df_crimes.shape)
print(df_crimes_filtered.shape)
print(df_crimes_filtered['Borough'].value_counts())

# Next we want to filter out anything in the crimes data WITHOUT a CrimeID, as without that we can't determine an outcome
# from the outcomes data
print("Before DropNA on Crime ID column")
print(df_crimes_filtered.shape)
df_crimes_filtered = df_crimes_filtered.dropna(subset=['Crime ID'])
print("After DropNA on Crime ID column")
print(df_crimes_filtered.shape)

# Now we merge crime and outcome data using the CrimeID. We are only interested in rows where;
# 1. We have a full row of data in the crimes dataframe
# 2. We have an outcome type in the outcomes dataframe
# We use LEFT to retain all rows with Crime IDs in 'crimes' then remove the blank Outcome Type rows after the merge.
print("Merging Crimes and Outcomes..")
df_merged = pd.merge(df_crimes_filtered, df_outcomes, on="Crime ID",how="left")
df_merged_filtered = df_merged.dropna(subset=['Outcome type'])

# Now we want to merge the Key Indicators data based on London Borough
print(df_merged.columns)
print(df_merged.shape)
# Do the merge
print('do the merge...')
df = pd.merge(df_crimes_filtered, df_keyindicators, on="Borough",how="left")
df.to_excel('df.xlsx')

print(df.columns)
print(df.shape)





