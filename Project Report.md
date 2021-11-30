# FIL Course - Final Assessment
## Project Report

### GitHub URL 
https://github.com/tallguy999/fil-course-assessment

### Abstract
An analysis of publicly available street crime data for the Metropolitan police, to determine how the pandemic and subsequent lockdowns may have impacted either the amount of crime committed or the type of crimes committed.

### Introduction
(Explain why you chose this project use case)

### Dataset
(Provide a description of your dataset and source. Also justify why you chose this source)

The main dataset consists of 2020 street crime data for the Metropolitan Police, published under the Open Government License 3.0.(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) and available for download from https://data.police.uk. Data is available for all UK police forces, but for the purpose of this exercise I have focused on the Metropolitan Police. 

Additional data has been obtained from https://www.trustforlondon.org.uk/data/boroughs/overview-of-london-boroughs/. This contains ratings for key indicators across all London Boroughs, including;
* Poverty Rate
* Income Inequality
* Pay Inequality
* Rough Sleeping
* Unemployment Rate

This will be merged with the street crime data to provide more features for the machine learning analysis.

The main street crime data is in CSV format and comprises the following fields;

#### Field Meaning

##### Reported by
The force that provided the data about the crime.

##### Falls within
Also the force that provided the data about the crime.

##### Longitude and Latitude
The anonymised coordinates of the crime.

##### LSOA code and LSOA name
References to the Lower Layer Super Output Area that the anonymised point falls into, according to the LSOA boundaries provided by the Office for National Statistics.

##### Crime type
One of the crime types listed in the Police.UK FAQ.

##### Last outcome category
A reference to whichever of the outcomes associated with the crime occurred most recently.

##### Context
A field provided for forces to provide additional human-readable data about individual crimes. Currently, for newly added CSVs, this is always empty.

### Implementation Process
(Describe your entire process in detail)

### Results
(Include the charts and describe them)

### Insights
(Point out at least 5 insights in bullet points)

### References
#### LSOA
Lower Layer Super Output Areas (LSOA) are a geographic hierarchy designed to improve the reporting of small area statistics in England and Wales. LSOAs have an average population of 1500 people or 650 households. 
Read more at; https://data.london.gov.uk/dataset/lsoa-atlas