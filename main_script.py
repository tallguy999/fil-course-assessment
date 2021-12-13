import functions_script as mf
import pandas as pd

# Create a dataframe from the London Borough Profiles data (Remote XLSX)
profiles_url = 'https://data.london.gov.uk/download/london-borough-profiles/80647ce7-14f3-4e31-b1cd-d5f7ea3553be/london-borough-profiles.xlsx'
df_profiles, boroughs = mf.Get_Profiles(profiles_url)
mf.ExportExcel(df_profiles, 'df_profiles')

# Create a dataframe from the crimes data (CSV)
# Pass the name of the CSV file plus the boroughs list to filter out non-London regions
# Pass the Crime type to filter on a specific crime
df_crimes = mf.Get_Crimes('sample_crimes.csv', boroughs, 'Drugs')
mf.ExportExcel(df_profiles, 'df_crimes')

# Create a dataframe from the Key Indicators data (Remote SQL)
df_keyindicators = mf.Get_Key_Indicators()
mf.ExportExcel(df_keyindicators, 'df_key_indicators')


df = pd.merge(df_crimes, df_profiles, on="Borough",how="left")
df = pd.merge(df, df_keyindicators, on="Borough",how="left")
mf.ExportExcel(df, 'df')
