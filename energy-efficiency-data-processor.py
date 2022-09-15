# ENERGY EFFICIENCY DATA PROCESSOR
# Living Rent, 2022
# --------------------------------

# PROGRAM DESCRIPTION:
# This program processes raw data from the Scottish Government on the energy efficiency of homes.
# The raw data can be downloaded from here:
#       https://statistics.gov.scot/data/domestic-energy-performance-certificates

# The data contains information on energy efficiency assessments which have been completed each quarter since 2012. Each quarter has its own CSV file.
# This program finds the most up to date assessment results on each home across all of the raw data. The program assumes that the newest files contain the most up to date information.

# It outputs:
#       * All data on every address that has been assessed since 2012 in a single CSV file (around 1.5 million homes as of September 2022)
#       * Individual CSV files for each local authority


# HOW TO USE:
# 1. Place all of the raw CSV files from the Scottish Government in the "raw-input" directory
# 2. Run this program - e.g., "python energy-efficiency-data-processor.py"

# Note: some data is removed to save on file size - only information relevant to Living Rent is processed. To get other available data, you can modify "columns_to_export" variable.


import csv, os, glob

# Keep track of unique, known addresses
known_addresses = {}
duplicate_addresses = 0

# Store unique addresses by their local authority
sorted_by_local_authorities = {}

# Specify which columns to export
# Note: local authority must be the first column
columns_to_export = ["Local Authority", "\ufeffProperty_UPRN", "OSG_UPRN", "ADDRESS1", "ADDRESS2", "POST_TOWN", "Postcode", "Tenure", "Property Type", "Date of Assessment", "Date of Certificate", "Current energy efficiency rating", "Current energy efficiency rating band", "Potential Energy Efficiency Rating", "Potential energy efficiency rating band", "Current Environmental Impact Rating", "Current Environmental Impact Rating Band", "Potential Environmental Impact Rating", "Potential Environmental Impact Rating Band", "CO2 Emissions Current Per Floor Area (kg.CO2/m²/yr)", "Improvements", "Ward Code", "Ward Name", "Data Zone 2011"]


print("ENERGY EFFICIENCY DATA PROCESSOR")
print("--------------------------------")
print("Living Rent, 2022")


print("\nGetting input files...")

# Get all CSV files in "raw-input" directory
input_files = []

for filename in glob.glob('raw-input/*.csv'):
    input_files.append(filename)
# Sort list of files so that the newest data comes first, i.e. "2022Q1.csv", "2021Q4.csv", "2021Q3.csv", etc.
input_files.sort(reverse=True)

print("Total of " + str(len(input_files)) + " input CSV files found in the \"raw-input\" directory")

print("\nProcessing raw input data files...")

# Iterate through each raw data input file
for input_filename in input_files:
    with open(input_filename) as input_file:
        # Open current input file as dictionary
        raw_reader = csv.DictReader(input_file, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)

        # Iterate through each address data in current input file
        for row in raw_reader:
            # Find Unique Property Reference Number (used as key for storing data and excluding duplicate entries for same address)
            uprn = row["\ufeffProperty_UPRN"]

            # If UPRN already exists, disregard data as it is out of date
            if uprn in known_addresses:
                duplicate_addresses += 1
            else:
                # Create empty list current address data, store inside kv pair where key is UPRN
                known_addresses[uprn] = []
                # Only store data from columns specified in "columns_to_export" list
                for column_name in columns_to_export:
                    known_addresses[uprn].append(row[column_name])

print("\nTotal unique addresses found: " + str(len(known_addresses)))
print("Total duplicate addresses found: " + str(duplicate_addresses))

print("\nWriting all data (unsorted) to the \"formatted-output\" directory...")

# Write processed data into one big CSV file and sort by local authority
with open('formatted-output/Energy Efficiency Data - All Local Authorities.csv', 'w') as unsorted_output_file:
    unsorted_writer = csv.writer(unsorted_output_file)

    # Write headers to output file
    unsorted_writer.writerow(columns_to_export)

    # Iterate through each address that has been processed
    for uprn in known_addresses:
        # Get address data from UPRN as local variable
        address = known_addresses[uprn]
        # Write address data to big output file
        unsorted_writer.writerow(address)

        # Sort data by local authority
        # Find local authority - assume it is the first (0th) element in list
        local_authority = address[0]

        # Setup of kv pair for all local authorities
        if local_authority == "":
            # Handle blank local authority
            local_authority = "Uncategorised"
        if local_authority not in sorted_by_local_authorities:
            sorted_by_local_authorities[local_authority] = []
        
        sorted_by_local_authorities[local_authority].append(address)

print("\nWriting data sorted by local authority to the \"formatted-output/by-local-authority\" directory...")

# Write processed data sorted by local authority
# Iterate through each local authority
for local_authority in sorted_by_local_authorities:
    with open("formatted-output/by-local-authority/" + local_authority + " - Energy Efficiency Data.csv", "w") as local_authority_output_file:
        local_authority_writer = csv.writer(local_authority_output_file)
        
        # Write headers to current local authority output file
        local_authority_writer.writerow(columns_to_export)

        # Iterate through each address in current local authority
        for address in sorted_by_local_authorities[local_authority]:
            local_authority_writer.writerow(address)

print("\nDone!")
