# FIL Course - Final Assessment
## Project Report

### GitHub URL 
https://github.com/tallguy999/fil-course-assessment

### Abstract
An analysis of publicly available London street crime data and London Borough Profile data, to 
determine whether or not London Borough Profile data can be used to predict the amount of reported crime. 

### Introduction
(Explain why you chose this project use case)

### Dataset
(Provide a description of your dataset and source. Also justify why you chose this source)

There are three sets of data used in this exercise;

#### Street Crime Data
Source: https://data.police.uk

License: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

The main dataset consists of street crime data for the Metropolitan Police. This is published under the Open Government 
License 3.0. This data is available for all UK police forces, but for the purpose of this exercise I have focused on 
the Metropolitan Police.

The data comprises the following fields;

- Reported by
    - The force that provided the data about the crime.
- Falls within
    - Also the force that provided the data about the crime.
- Longitude and Latitude
    - The anonymised coordinates of the crime.
- LSOA code and LSOA name
    - References to the Lower Layer Super Output Area that the anonymised point falls into (See References)
- Crime type
    - One of the crime types listed in the Police.UK FAQ.
- Last outcome category
    - A reference to whichever of the outcomes associated with the crime occurred most recently.
- Context
    - A field provided for forces to provide additional human-readable data about individual crimes.
    - Currently, this is always empty.

#### London Borough Profiles
Source: https://data.london.gov.uk/download/london-borough-profiles/80647ce7-14f3-4e31-b1cd-d5f7ea3553be/london-borough-profiles.xlsx

License: http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/

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



##### Data Quality Issues

- The data provided covers a wide time span, dating from March 2011 to March 2016, so even the most recent data is 
already over 5 years old. However the dates for each metric are consistent across all the London Boroughs.

 Therefore prior to import, the Profiles and Chart-Map worksheets were deleted
and the remaining Data tab saved as a CSV file (London-Borough-Profiles.csv). The original .XLSX file has been included 
in the project for reference.

### Implementation Process
(Describe your entire process in detail)

### Results
(Include the charts and describe them)

### Insights
(Point out at least 5 insights in bullet points)

### References
#### LSOA
Lower Layer Super Output Areas (LSOA) are a geographic hierarchy designed to improve the reporting of small area 
statistics in England and Wales. LSOAs have an average population of 1500 people or 650 households. 
Read more at; https://data.london.gov.uk/dataset/lsoa-atlas