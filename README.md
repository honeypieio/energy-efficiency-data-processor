# Energy Effiency Data Processor

Living Rent, September 2022



### Program Description
This program processes raw data from the Scottish Government on the energy efficiency of homes.

The raw data can be downloaded from here: [https://statistics.gov.scot/data/domestic-energy-performance-certificates](https://statistics.gov.scot/data/domestic-energy-performance-certificates)

The data contains information on energy efficiency assessments which have been completed each quarter since 2012. Each quarter has its own CSV file. This program finds the most up to date assessment results on each home across all of the raw data. The program assumes that the newest files contain the most up to date information.

It outputs:
 - All data on every address that has been assessed since 2012 in a single CSV file (around 1.5 million homes as of September 2022) 
 - Individual CSV files for each local authority

### How To Use
 1. Place all of the raw CSV files from the Scottish Government in the "raw-input" directory
 2. Run this program - e.g., `python energy-efficiency-data-processor.py`

Note: some data is removed to save on file size - only information relevant to Living Rent is processed. To get other available data, you can modify "columns_to_export" variable.

### Prerequisites
 - Python 3
