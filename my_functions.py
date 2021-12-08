import pandas as pd
import openpyxl

def ExportToExcel(df, filename='dump.xlsx'):
    # Write the <df> to an Excel file named <filename>
    # If the filename argument does not end in '.xlsx' append it here
    last_chars = filename[-5:]
    if last_chars != ".xlsx":
        filename = filename + '.xlsx'
    df.to_excel(filename)
    return(filename)

def Process_Profiles(filename):
    # This function will import and process the London Borough Profiles data and return a dataframe
    # to be merged with the crime data, joined by Borough.

    c1 = ['Borough', 'Inner or Outer','Population', 'Area (Hectares)']
    c2 = ['Population Density', 'Average Age','Youth Unemployment']
    c3 = ['Median House Price', 'Rented Local Authority']
    columns = c1 + c2 + c3
    df = pd.read_csv(filename, usecols = columns)

    # For the Inner or Outer Column, replace Inner with 0 and Outer with 1
    # Then rename the column 'Outer'
    df['Inner or Outer'].replace(['Inner London'], 0, inplace=True)
    df['Inner or Outer'].replace(['Outer London'], 1, inplace=True)
    df.rename(columns={'Inner or Outer': 'Outer'}, inplace=True)

    # After checking the missing values across this dataframe, there is one in the 'Rented Local Authority' column
    # for the City of London. Bearing in mind the amount of local authority housing in the City of London (effectively
    # the 'Square Mile') would be very low, we'll take the lowest value in this column (Richmond upon Thames = 8.7),
    # halve it and then update the City of London with this value.

    print("Checking for missing values;")
    print(df.isna().sum(axis = 0))

    print("..............................")
    print("Before:", df.loc[0, ['Borough', 'Rented Local Authority']])
    df.loc[df['Borough'] == 'City of London', 'Rented Local Authority'] = df['Rented Local Authority'].min()/2
    print("After:", df.loc[0, ['Borough', 'Rented Local Authority']])
    print("..............................")

    print("Checking for missing values;")
    print(df.isna().sum(axis = 0))

    return df

def Restructure_Outcomes(df):
    df = df.replace({'Outcome type': 'Investigation complete; no suspect identified'}, 0)
    df = df.replace({'Outcome type': 'Suspect charged'}, 1)
    df = df.replace({'Outcome type': 'Offender given penalty notice'}, 1)
    df = df.replace({'Outcome type': 'Offender given a drugs possession warning'}, 1)
    df = df.replace({'Outcome type': 'Offender given a caution'}, 1)
    df = df.replace({'Outcome type': 'Local resolution'}, 1)
    df = df.replace({'Outcome type': 'Formal action is not in the public interest'}, 1)


    print(df)
    exit(1000)
    return df