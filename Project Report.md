# FIL Course - Final Assessment
## Project Report

### GitHub URL 
https://github.com/tallguy999/fil-course-assessment

### Abstract
An analysis of publicly available London street crime data and London Borough Profile data, to 
determine whether or not there is any correlation between London Borough key metrics and the amount of reported crime. 

### Introduction
I have previously worked with Police crime data with a view to understanding the impact of the COVID pandemic, in particular
the impact of COVID lockdowns on the amount of reported street crime, therefore it is a dataset of which I have some familiarity.
Having also spent a few years working in the Metropolitan Police as a serving police officer I have some understanding of 
the makeup of London and it's boroughs in relation to crime.

### Dataset
There are three sets of data used in this exercise; 

#### Street Crime Data
Source: https://data.police.uk

License: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

Import Method: Data read directly from downloaded CSV file.

This data consists of reported street crimes. It is published under the Open Government License 3.0 and is available 
for all UK police forces, but for the purpose of this exercise I have focused on the Metropolitan Police.

The data is almost entirely categorical in nature and comprises the following fields;

- "Reported by" and "Fall within"
    - The force that provided the data about the crime.
- Longitude and Latitude
    - The anonymised coordinates of the crime.
- LSOA code and LSOA name
    - References to the Lower Layer Super Output Area that the anonymised point falls into (See References)
- Crime type
    - One of the crime types listed in the Police.UK FAQ.
- Last outcome category
    - A reference to whichever of the outcomes associated with the crime occurred most recently. This can be cross referenced with a separate 'Outcomes' dataset, but is not used in this exercise.
- Context
    - A field provided for forces to provide additional human-readable data about individual crimes. Currently, this is always empty.
    
Apart from the reference to the 'Crime type' and a location, there is no other detail of the actual crime itself. So any kind of analysis
focusing on the actual crime will always be fairly limited. Therefore I decided to summarise and count the data to provide borough-specific
quantative metrics (total crimes in each borough) that I could then match up with the borough profile and key indicators to data, to provide a
spread of numeric data to use in machine learning and linear regression.

#### London Borough Profiles
Source: https://data.london.gov.uk/download/london-borough-profiles/80647ce7-14f3-4e31-b1cd-d5f7ea3553be/london-borough-profiles.xlsx

License: http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/

Import Method: A custom function (Get_Profiles) is used to retrieve and process the data directly from the URL.

This data is provided as an Excel workbook containing three worksheets. The workbook consists of three worksheets; 
Profiles, Data and Chart-Map. We will only be using the information within the Data worksheet for this exercise.


This worksheet contains 82 features grouped into 11 themes for each London borough.
- Demography
- Diversity
- Labour Market
- Economy
- Community Safety
- Housing
- Environment
- Transport
- Children
- Health
- Governance

Note: The original Profiles worksheet contains source information for each feature.

#### Borough Ratings Across Key Indicators (2021)
Source: https://www.trustforlondon.org.uk/data/boroughs/overview-of-london-boroughs/

License: Unable to locate license info on website, though data appears to be collected from a number of different sources which are referenced.

Import Method: In order to demonstrate the import of data from a SQL database, a subset of this data was taken from the CSV file and 
uploaded to remote SQL server, then downloaded into the script using a custom function (Get_Key_Indicators)

Further borough specific metrics focused on poverty, homelessness, unemployment etc.

##### Data Quality Issues

- The data provided in the London Borough Profiles covers a wide time span, dating from March 2011 to March 2016, so even the most recent data is 
already over 5 years old. However the dates for each metric are consistent across all the London Boroughs. Key Indicators data is the most relevant 
being published in 2021.

- Crime data can be downloaded for 2018 through to 2021. From previous analysis of data collected during the pandemic, I'm aware that COVID lockdowns 
had a significant impact on the amount of reported crime during 2020, therefore I decided to avoid this time period completely and focus
on pre-pandemic data (2019).

### Implementation Process
1. Create three dataframes from the London Borough Profiles, Crime and Key Indicators data by calling three custom 
functions (All defined in functions_script.py). Each function imports the data then performs data manipulation and cleansing;

- mf.Get_Profiles(url)
    - Retrieves London Borough Profile data from remotely-hosted Excel workbook at location specified by 'url'.
    - Uses the *sheet_name* parameter to specify the worksheet to load (There are three in the workbook).
    - Uses the *usecols* parameter to specify the columns to load (We don't need all 82 columns).
    - Drop the last 6 row. These contain summed totals for Inner London, Outer London, London, England and UK.
    - Drop the first row which is blank.
    - Change the *Inner/ Outer London* column from a text column to a numeric column, by replacing instances of *Inner* 
    with 1 and *Outer* with 0, then rename the column to *Inner*.
    - Rename the remaining columns using the Excel file Profile_Column_Mapping.xlsx to map a new name against the old name.
    - Handle missing values;
        - Missing values in this file are identifed with a period (.) character. These don't get picked up by functions 
        such as *isnull()* and *dropna()*. 
        - Use a *RegEx* expression to find single period characters and replace them with a Numpy NaN value.
            - Change the debug value at the top of functions_script.py to 1 to get printed output of this process.
        - Rented_Local_Authority percentage for the City of London is missing. Although the City of London does have
        some local authority housing, it is minimal and I've been unable to find the exact figures. For the purpose of
        this exercise we'll use half the lowest value in that column - Using df.loc to find and replace those values.
        - Gender-specific employment and unemployment figures are also missing for the City of London.
        - The total Employment figure for the City is 64% which is 8 points below the average. On that basis we will take 
        the average values for Percent_Employed_Male and Percent_Employed_Female and reduce those by 8% for the City.
     - Use the values in the *Boroughs* column to create a list of London Boroughs. This is used as a filter on the crimes data.   
    - Return a dataframe as *df*
    - Return the Boroughs list as *boroughs*
    
- mf.Get_Crimes(filename, boroughs, crime)
    - Pass the name of the downloaded file, together with a list containing the names of the London Boroughs and a second
    list specify the crime (or crimes) you want to filter on.
    - Read the CSV into a data frame.
        - Use the *usecols* parameter to load only the *LSOA name* and *Crime type* columns.
    - The *LSOA name* columns consists of two values;
        - The LSOA code (See LSOA in *References* below)
        - The name of a geographic region,
    - Split out the LSOA code from the region name using str.rpartition()
    - Use the region name to create a new column and drop the original *LSOA name* column.
    - Filter on the new *Borough* column using the *boroughs* list, to remove all non-London regions.
    - Filter on the *Crime type* column using the *crime* parameter.
    - Finally use *groupby*, *count* and *sort* to create a new dataframe listing total crimes by Borough.
    - Rename the *Crime type* column to *Crime Count*.
    - Returns this dataframe as *df*
    
- mf.Get_Key_Indicators
    - Use the mysql.connector to retrieve the data hosted on remote SQL.
    - Pass the SQL query to specify the columns to retreive.
    - Returns dataframe as *df*
    
2. Merge the three dataframes into one dataframe (df); df_crimes, df_profiles and df_keyindicators on the *Borough* column, using pd.merge with the argument *how = "left"*.

3. Prepare for Linear Regression processes

Here we will try to predict if the London Borough Profile and Key Indicators data can be used to predict the 
amount of crime committed.

- Drop the *Boroughs* column as it is non-numeric and will cause errors.
- Create the target and feature arrays;
    - Drop the *Crime Count* column, leaving all other features and assigning to *X*
    - Slice out the *Crime Count* column to create the target array; *y*
    
Then perform the following processes in order;

    1. Linear Regression using Train_Test_Split (Line 60 of main_script.py)
    This yields a score of -10.035372743519426
    
    2. Linear Regression with Cross Validation (Line 70 of main_script.py)
    Returns [-0.27704644 -0.44870099  0.12954645  0.07383437 -0.71928945]
    Average 5-Fold CV Score: -0.24833121150287346
    
    3. Ridge Regression (Line 78 of main_script.py)
    This yields a score of -0.04579818315864226
    
    4. Lasso Regression (Line 88 of main_script.py)
    This yields a score of 0.27862015698673825
    
    5. HyperParameter Tuning - Grid Search CV with Ridge Regression (Line 98 of main_script.py)
    GridSearch / Best Params:  {'alpha': 49}
    GridSearch / Best Score:  -0.8034345345065449
    
Lastly, we use Lasso for feature selection, plotting coefficients to determine the best features for prediction. This 
appears to generate an error, but unsure as to what this means or how to resolve it. I think it may have something to
do with the limited amount of data I'm working with?

> ConverganceWarning: Objective did not converge. You might want to increase the number of interations, check the scale
of the features or consider increasing regularisation.



    

### Results
(Include the charts and describe them)

### Insights
(Point out at least 5 insights in bullet points)

### References
#### LSOA
Lower Layer Super Output Areas (LSOA) are a geographic hierarchy designed to improve the reporting of small area 
statistics in England and Wales. LSOAs have an average population of 1500 people or 650 households. 
Read more at; https://data.london.gov.uk/dataset/lsoa-atlas