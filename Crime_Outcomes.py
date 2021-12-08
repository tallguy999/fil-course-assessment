import pandas as pd
import mysql.connector as sql
import openpyxl
import my_functions as myfunctions
debug = 0

db_connection = sql.connect(user='me0RUcEKLC',password='NYzWbTM2H6',host='remotemysql.com',database='me0RUcEKLC')
pd.options.display.max_columns = 50

# Crimes and Outcomes data is imported from the CSV files downloaded from https://data.police.uk/data/
# For the purpose of demonstrating the import of data from a relational database, the Key Indicators data was first
# downloaded from https://data.police.uk/data/ and then imported to a remote MySQL database at https://remotemysql.com.
# An additional data set, London Borough Profiles, is imported from another CSV file. This builds on the data from the
# Key Indicators data and provides additional values and scores that can be tied to each London Borough.

df_crimes = pd.read_csv('sample_crimes.csv', usecols=['Crime ID', 'LSOA name', 'Crime type'])
df_outcomes =  pd.read_csv('sample_outcomes.csv', usecols=['Crime ID', 'Outcome type'])
df_keyindicators = pd.read_sql('SELECT * FROM KEY_INDICATORS', con=db_connection)
df_profiles = myfunctions.Process_Profiles('London-Borough-Profiles.csv')

# PROCESSING THE CRIMES DATA;
# Split the 'LSOA name' column using rpartition(). rpartition results in a dataframe ('result') comprising 3 columns;
# Column[0] The Region, Column[1] A Space, Column[2] The LSOA Code
# Use column [0] to create a new Borough column then drop the original 'LSOA name' column

result = df_crimes['LSOA name'].str.rpartition()
df_crimes['Borough'] = result[0]
df_crimes.drop('LSOA name', axis=1, inplace=True)

# The crimes data contains a small number of crimes (0.45%) committed outside the Greater London area.
# We only want data that can be specifically tied to a London Borough.
# To find and remove the crimes not committed in London;
#   Use 'groupby' and 'count' on the 'Borough' column to create a list ordered by count of unique values.
#   Use 'head' to extract the top 33 rows.

Borough_summary = df_crimes.groupby(['Borough']).Borough.count()
sorted_Borough_summary = Borough_summary.sort_values(ascending=False)

data = sorted_Borough_summary.head(33)
boroughs = data.index.to_list()

# Now we have a list of London Boroughs, we use that list to filter out all the Non-London regions in the Crimes data
df_crimes = df_crimes[df_crimes['Borough'].isin(boroughs)]

# By doing a count of unique values in the Borough column we should be left with a list of the 33 London Boroughs
print(df_crimes['Borough'].value_counts())

# Next we want to filter out anything in the Crimes data WITHOUT a CrimeID, without that we can't determine an outcome
# when we merge the Outcomes dataframe, so this needs to be removed.
df_crimes = df_crimes.dropna(subset=['Crime ID'])

# Also drop rows where 'Crime type' is shown as the generic 'Other crime' or 'Other theft'
df_crimes = df_crimes[df_crimes['Crime type']!= 'Other crime']
df_crimes = df_crimes[df_crimes['Crime type']!= 'Other theft']

# MERGE CRIMES AND OUTCOME DATA
# Now merge 'crime' and 'outcome' data using 'CrimeID'. We are only interested in rows where;
# 1. We have a full row of data in the crimes dataframe
# 2. We have an outcome type in the outcomes dataframe
# Use LEFT to retain all rows with Crime IDs in 'crimes' then remove the rows with missing 'Outcome Type'.
df_crimes = pd.merge(df_crimes, df_outcomes, on="Crime ID",how="left")
df_crimes = df_crimes.dropna(subset=['Outcome type'])
myfunctions.Restructure_Outcomes(df_crimes)

# MERGE THE KEY INDICATORS DATA
# Now we merge the Key Indicators data based on London Borough and assign to our main dataframe; df
df_crimes = pd.merge(df_crimes, df_keyindicators, on="Borough",how="left")

# MERGE THE LONDON BOROUGH PROFILES DATA
df_crimes = pd.merge(df_crimes, df_profiles, on="Borough",how="left")

myfunctions.ExportToExcel(df_crimes, 'df_crimes')








