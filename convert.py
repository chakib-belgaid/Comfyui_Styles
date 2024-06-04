import csv
import json
import sys
import os


# Open the CSV file and read its contents
# Get the input file path from command line arguments
input_file = sys.argv[1]

# Get the file name without extension
file_name = os.path.splitext(input_file)[0]

# Open the CSV file and read its contents
with open(input_file, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    headers = next(reader)  # Skip the header row

    # Create a list of dictionaries, each representing a row in the CSV
    csv_list = [dict(zip(headers, row)) for row in reader]

# Convert the list into JSON format and write it to a file
output_file = f"{file_name.replace('.csv', '')}.json"
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(csv_list, json_file, indent=4)

# Return the output file path
output_file
