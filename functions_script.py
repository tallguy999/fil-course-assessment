import pandas as pd
import numpy as np
import seaborn as sns
import mysql.connector as sql
import openpyxl
pd.options.display.max_columns = 50
debug = 0

def ExportExcel(df, filename='dump.xlsx'):
    # Write the <df> to an Excel file named <filename>
    # Append '.xlsx' if the file extension is not supplied.
    last_chars = filename[-5:]
    if last_chars != ".xlsx":
        filename = filename + '.xlsx'
    df.to_excel(filename)

    return(filename)

def Get_Crimes(filename, boroughs, crime):
    df = pd.read_csv(filename, usecols=['LSOA name', 'Crime type'])

    # PROCESSING THE CRIMES DATA;
    # Split the 'LSOA name' column using rpartition(). rpartition results in a dataframe ('result') with 3 columns;
    # Column[0] The Region, Column[1] A space, Column[2] The LSOA Code
    # Use column [0] to create a new Borough column then drop the original 'LSOA name' column

    result = df['LSOA name'].str.rpartition()
    df['Borough'] = result[0]
    df.drop('LSOA name', axis=1, inplace=True)

    # Use the passed boroughs list to filter out the non-London regions
    df = df[df['Borough'].isin(boroughs)]
    # Use the passed 'crime' value to filter out the unwanted crime types
    df = df[df['Crime type'].isin(crime)]

    df = df.groupby(['Borough']).count()
    df.sort_values(by=['Borough'], inplace=True)
    df.rename(columns={'Crime type': 'Crime Count'}, inplace=True)
    print(df)

    return df

def Get_Profiles(url):
    # The London Borough Profiles data has 82 columns - we don't want/need all of these, so specify the ones we want here
    cols_1 = ['Area name', 'Inner/ Outer London']
    cols_2 = ['GLA Population Estimate 2017', 'GLA Household Estimate 2017', 'Inland Area (Hectares)', 'Population density (per hectare) 2017']
    cols_3 = ['Proportion of population aged 0-15, 2015', 'Proportion of population of working-age, 2015', 'Proportion of population aged 65 and over, 2015']
    cols_4 = ['Employment rate (%) (2015)', 'Male employment rate (2015)', 'Female employment rate (2015)', 'Unemployment rate (2015)']
    cols_5 = ['Youth Unemployment (claimant) rate 18-24 (Dec-15)', 'Rented from Local Authority or Housing Association, (2014) %']
    profiles_columns = cols_1 + cols_2 + cols_3 + cols_4 + cols_5
    df = pd.read_excel(url, sheet_name='Data', usecols=profiles_columns)

    # Remove the last 6 rows. These relate to areas outside the actual boroughs (e.g. inner London,
    # outer London, London, England and UK) (1-5) and a row of summed values across all the columns (6).
    df = df.iloc[:-6]
    # Drop the first row which is blank
    df.drop(index=0, inplace=True)

    # For the 'Inner/ Outer London' column, set the value to 1 if inner or 0 if outer.
    filter_inner = (df['Inner/ Outer London'] == 'Inner London')
    filter_outer = (df['Inner/ Outer London'] == 'Outer London')
    df.loc[filter_inner, 'Inner/ Outer London'] = 1
    df.loc[filter_outer, 'Inner/ Outer London'] = 0

    # Rename the columns according to the mappings in Profile_Column_Mapping.xlsx
    new_column_names = pd.read_excel('data/Profile_Column_Mapping.xlsx')
    new_column_names = new_column_names['New'].values.tolist()
    df.columns = new_column_names

    # Missing values are identified with a single '.', which means functions such as .isnull() and
    # .dropna() won't pick these up. Use RegEx to find those single "." characters and use Numpy to
    # replace with a NaN value.
    if debug:
        print("Before RegEx Replacement:")
        for index, row in df.iterrows():
            if (pd.isnull(row['Rented_Local_Authority'])):
                print("Null values found in row:", index)
                print(row)
        print("---------")

    df = df.replace(to_replace=r'^.$', value=np.nan, regex=True)

    if debug:
        print("After RegEx Replacment:")
        for index, row in df.iterrows():
            if (pd.isnull(row['Rented_Local_Authority'])):
                print("Null values found in row:", index)
                print(row)
        print("---------")

    # The Rented_Local_Authority percentage for the City of London is missing.
    # The City of London has very little in way of Local Authority Housing, although it does have some. I've been unable
    # to get the actual figures, so for our purposes we will just use half of the lowest value in the column.
    df.loc[df['Borough'] == 'City of London', 'Rented_Local_Authority'] = df['Rented_Local_Authority'].min() / 2


    # Specific male and female Employment and Unemployment figures are also missing for the City. The total Employment
    # figure for the City is 64% which is 8 points below the average. On that basis we will take the average values
    # for Percent_Employed_Male and Percent_Employed_Female and reduce those by 8% for the City.
    df.loc[df['Borough'] == 'City of London', 'Percent_Employed_Male'] = int(df['Percent_Employed_Male'].mean() * 0.92)
    df.loc[df['Borough'] == 'City of London', 'Percent_Employed_Female'] = int(df['Percent_Employed_Female'].mean() * 0.92)
    df.loc[df['Borough'] == 'City of London', 'Unemployment_Rate'] = int(df['Unemployment_Rate'].min() / 2)


    # Use the Borough dataframe column to create a list of Boroughs
    # This will be used on the Crimes data to filter out Non-London regions
    boroughs = df['Borough'].values.tolist()
    return df, boroughs

def Get_Key_Indicators():
    db_connection = sql.connect(user='me0RUcEKLC', password='NYzWbTM2H6', host='remotemysql.com', database='me0RUcEKLC')
    df = pd.read_sql('SELECT Benefits, Borough, Child_Poverty, Homelessness, Income_Inequality, Median_Rent, Poverty, Repossessions, Sleeping_Rough FROM KEY_INDICATORS', con=db_connection)
    return df



