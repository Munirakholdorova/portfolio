---
title: "Mini Project2"
excerpt_separator: "<!--more-->"
categories:
  - project1
tags:
  - experiments
  - Mini Project
image: images/healthcare-12-00686-g002.png
---

### Mini Project Proposal: Digital Analysis of Trust, Risk, and Reputation in Undocumented Migrant Labour Networks

For my Mini Project, I ask Which economic sectors employ the highest number of unauthorized migrant workers? Because these workers are often hidden from official records, the data is not direct and will need integration from several data sets. By applying DH methods, the work combines public government datasets, OCR extraction of statistical tables, and Python-based NER analysis to explore labour patterns among migrants. 


<!--more-->

### Data Corpus#

My corpus will come from six data sets The corpus includes publicly available datasets relevant to the question. Each source contributes sectoral, demographic, or labour-market variables needed for comparative analysis. These datasets contain downloadable CSVs, Excel files, and PDF-based statistical releases that requires OCR.

## Data Sources#

[Migration and the Labour Market, England and Wales: Census 2021 (ONS)](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/articles/migrationandthelabourmarketenglandandwales/census2021) 

[Ethnicity Facts & Figures – Employment by Sector (UK Government)](https://www.ethnicity-facts-figures.service.gov.uk/work-pay-and-benefits/employment/employment-by-sector/latest/#data-sources)

[UK Labour Market Bulletin: Employment and Employee Types (ONS)](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/uklabourmarket/2015-10-14)

[Annual Survey of Hours and Earnings (ASHE) linked to 2011 Census](https://datacatalogue.adruk.org/browser/dataset/124775/1/1034719)

[Immigration System Statistics (UK Government):  These enforcement-related datasets are used for information on sectors and for samples of unauthorized work and arrest](https://www.gov.uk/government/statistics/immigration-system-statistics-year-ending-september-2025)

[Illegal Working & Returns Statistical Releases (selected tables only for contextual separation of authorized vs unauthorized work)](https://www.gov.uk/government/publications/returns-from-the-uk-and-illegal-working-activity-since-july-2024)
 
## Digital Humanities Process

### Data Collection and OCR with eScriptorium#
After downloading the datasets, PDF based statistical tables must be extracted with OCR. Using eScriptorium and a numerically oriented OCR model suitable for statistical documents, it could be exported to results in structured formats like csv. 

### Data Cleaning#
Cleaning includes correcting OCR digit errors, removing stray characters, and retaining only key variables such as sector, migrant status, year, and work-visa category. This  will create compatible datasets ready for integration.

### Data Integration#
Python pandas is used to merge the datasets. Each cleaned CSV is loaded into a DataFrame. This allows datasets to be aligned and migrant employment variables to be combined across sources. Integration also includes filtering the data to include only unauthorized or illegal migrants based on visa categories or census classifications. Economic sector categories vary across sources, so a master list of standardized sectors is created. 

### Analysis with Python#

With integrated data, pandas is used to compute aggregated values such as the total number of migrant workers per sector. Grouping and sorting operations identify the most common sectors of unauthorized migrant employment. 

### Visualization in Python#
Data visualization is performed using matplotlib, which allows the creation of bar charts, pie charts, or simple line graphs comparing years. Visual representations support interpretation by clearly showing which sectors dominate migrant employment patterns. 

## Ethical Considerations#
Working with migration and labour data requires careful ethical reflection. Although the datasets are aggregated and publicly released, it is essential to avoid drawing simplistic or harmful conclusions about migrant communities or reinforcing stereotypes about the kinds of work migrants “typically” do. Government categories such as “migrant,” “work visa,” or “sector worker” are not neutral. They are products of specific administrative aims, policies, and political contexts. Their limitations must be acknowledged throughout the analysis. It is also important to distinguish clearly between authorized and unauthorized work and to avoid misinterpreting enforcement statistics. 


